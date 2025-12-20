from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from git import Repo

from dotify_lib import CACHE_DIR
from dotify_lib.namespace import Namespace
from dotify_lib.plugin import PluginManager
from dotify_lib.shell import Shell


@dataclass
class Config:
    depends: list[Path]
    actions: list[dict]


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

            tree_node = Config(depends=[], actions=config.get("actions", {}))

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
        observed: set[Path] = set()

        to_observe: deque[Path] = deque([root])
        while to_observe:
            node = to_observe.popleft()
            if node in observed:
                return False

            observed.add(node)
            for child in self.tree[node].depends:
                to_observe.append(child)

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
        actions = self.tree[path].actions
        for action in actions:
            if "procedure" not in action:
                print(f"[ERROR]: Unable to find procedure in config: {path}")
                exit(-1)

            shell = Shell(cwd=path.parent)
            if command := action.get("skip_if", None):
                if shell.run(command, privileged=action.get("privileged", False)) == 0:
                    print("[INFO]: Skipping this hook")
                    continue

            self.plugins.run_action(action, namespace=self.namespace, cwd=path.parent)

    def _clone_repository(self, url: str) -> Path:
        print(f"[INFO]: Cloning repository: {url}")
        user_name, user_repo = url.removesuffix(".git").split("/")[-2:]
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
