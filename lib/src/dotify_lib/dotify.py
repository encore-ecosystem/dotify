from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from git import Repo

from dotify_lib import CACHE_DIR
from dotify_lib.logger import log_critical, log_exception, log_info
from dotify_lib.namespace import Namespace
from dotify_lib.plugin import PluginManager
from dotify_lib.plugin.procedure import PluginProcedure
from dotify_lib.shell import Shell


@dataclass
class Config:
    depends: list[Path]
    actions: list[PluginProcedure]


@dataclass
class Dotify:
    plugins: PluginManager
    namespace: Namespace
    tree: dict[Path, Config] = field(default_factory=dict)
    order: deque = field(default_factory=deque)

    def apply(self, path: Path):
        path = self._predict_path(path)

        # step 1: Building dependency tree
        print("[INFO]: Building dependency tree...")
        self._build_subtree(path)

        # step 2: Validate tree
        print("[INFO]: Validating tree...")

        if not self._check_is_dag(path):
            print("[ERROR]: Found cycle!")
            exit(-1)

        # step 3: Build order
        print("[INFO]: Applying configs...")
        self._build_order(path)

        # step 4: Apply one-by-one
        while self.order:
            actual = self.order.popleft()
            print(f"[INFO]: Applying config: {actual}")
            self._apply(actual)

    def _build_subtree(self, path: Path):
        assert path.is_file()

        # Cache + prevent recursive trap
        if path in self.tree:
            return

        if self.is_config(path):
            with path.open("r") as source:
                config = yaml.safe_load(source) or {}

            actions: list[PluginProcedure] = []
            for action in config.get("actions", {}):
                if "procedure" not in action:
                    log_exception(f"Missing 'procedure' key in action: {path}")
                if (procedure := action["procedure"]).count(".") != 1:
                    log_exception(
                        f"Procedure <{procedure}> should be in format 'plugin_name.procedure': {path}"
                    )
                plugin_name, plugin_procedure_name = procedure.split(".")

                if plugin_name not in self.plugins.plugins:
                    log_exception(f"Plugin <{plugin_name}> not found: {path}")
                plugin = self.plugins.plugins[plugin_name]

                if plugin_procedure_name not in plugin.procedures:
                    log_exception(
                        f"Procedure <{plugin_procedure_name}> not found in plugin <{plugin_name}>: {path}"
                    )
                plugin_procedure_t = plugin.procedures[plugin_procedure_name]
                procedure_config = action.copy()
                del procedure_config["procedure"]

                actions.append(plugin_procedure_t(**procedure_config))

            tree_node = Config(depends=[], actions=actions)

            deps = config.get("depends", [])
            if not isinstance(deps, list):
                print(f"[ERROR]: Dependency section should be a list: {path}")
                exit(-1)

            for dep in deps:
                if dep.startswith("git+"):
                    repo = dep.replace("git+", "")
                    dep = self._clone_repository(repo)
                dep = Path(dep)
                if not dep.is_absolute():
                    dep = path.parent / dep
                dep = self._predict_path(dep.resolve())
                tree_node.depends.append(dep)

            self.tree[path] = tree_node
            for dep in tree_node.depends:
                self._build_subtree(dep)

        elif self.is_manifest(path):
            target_path = self._predict_path(path)
            if not target_path.exists():
                print(f"[ERROR]: Manifest directory not found: {path.parent}")
                exit(-1)
            self._build_subtree(target_path)

        else:
            print(f"[ERROR]: Unexpected file: {path}")
            exit(-1)

    def _check_is_dag(self, root: Path) -> bool:
        def dfs(
            node: Path,
            visited: set[Path],
            rec_stack: set[Path],
            parent_map: dict[Path, Path],
        ) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.tree[node].depends:
                parent_map[neighbor] = node
                if neighbor not in visited:
                    if not dfs(neighbor, visited, rec_stack, parent_map):
                        return False
                elif neighbor in rec_stack:
                    cycle_path = []
                    current = node
                    cycle_path.append(neighbor)
                    while current != neighbor and current in parent_map:
                        cycle_path.append(current)
                        current = parent_map[current]
                    cycle_path.append(neighbor)
                    cycle_str = " -> ".join(str(p) for p in reversed(cycle_path))
                    log_critical(f"Cycle detected: {cycle_str}")
                    return False

            rec_stack.remove(node)
            return True

        visited = set()
        start_node = root
        if start_node in self.tree:
            if not dfs(start_node, visited, set(), {}):
                return False

        for node in self.tree:
            if node not in visited:
                if not dfs(node, visited, set(), {}):
                    return False

        return True

    def _build_order(self, root: Path):
        indegree = {node: len(self.tree[node].depends) for node in self.tree}
        queue = deque([node for node, deg in indegree.items() if deg == 0])

        while queue:
            node = queue.popleft()
            self.order.append(node)

            for parent, entry in self.tree.items():
                if node in entry.depends:
                    indegree[parent] -= 1
                    if indegree[parent] == 0:
                        queue.append(parent)

    def _predict_path(self, path: Path) -> Path:
        if not path.is_dir():
            return path

        manifests_path = path / "dotify.toml"
        if manifests_path.exists():
            return manifests_path.parent / "manifests" / "main.yaml"

        main_yaml_path = path / "main.yaml"
        if main_yaml_path.exists():
            return main_yaml_path

        print(f"[ERROR]: Unable to predict path for: {path}")
        exit(-1)

    def _apply(self, path: Path):
        shell = Shell(cwd=path.parent)
        for action in self.tree[path].actions:
            if info := action.info:
                log_info(info)
            if condition := action.skip_condition:
                log_info("Found skip condition! Output is:")
                if shell.run(condition) == 0:
                    log_info("Output is 0. Skipping this action")
                    continue

            action.run(shell=shell, namespace=self.namespace)

    def _clone_repository(self, url: str) -> Path:
        if url.count("@") > 1:
            log_exception(f"Too many repository selectors: {url}")

        kwargs = {}
        selector = ""
        if url.count("@") == 1:
            selector = url.split("@")[1]
            if selector.count("=") != 1:
                log_exception(f"Invalid repository selector: {selector} in {url}")
            selector_name, selector_value = selector.split("=")
            match selector_name:
                case "branch":
                    kwargs = {"--branch": selector_value}
                case "tag":
                    kwargs = {"--tag": selector_value}
                case "commit":
                    kwargs = {"--commit": selector_value}
                case _:
                    log_exception(f"Unknown repository selector: {selector_name} in {url}")

        print(f"[INFO]: Cloning repository: {url}")
        user_name, user_repo = url.removesuffix("@" + selector).removesuffix(".git").split("/")[-2:]
        to_path = CACHE_DIR / user_name / user_repo
        if not to_path.exists():
            repo = Repo.clone_from(url, to_path)
        repo = Repo(to_path)
        repo.remotes.origin.pull()
        return to_path

    @staticmethod
    def is_manifest(path: Path) -> bool:
        return path.name == "dotify.toml"

    @staticmethod
    def is_config(path: Path) -> bool:
        return path.suffix == ".yaml"
