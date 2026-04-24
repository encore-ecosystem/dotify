from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from git import Repo

from dotify_lib import CACHE_DIR
from dotify_lib.logger import log_critical, log_exception, log_info
from dotify_lib.manifest import Manual, ProjectManifest
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

    def apply_manifest(self, path: Path):
        # step 1: Building dependency tree
        print("[INFO]: Building dependency tree...")
        self._build_subtree(path)

    def _build_subtree(self, path: Path):
        manifest = ProjectManifest.read(path / ProjectManifest.get_default_filename())
        if manifest is None:
            print(f"[ERROR]: No manifest file in {path}")
            exit(1)

        if manifest in self.tree:
            return

        manifest_manual_path = path / "manifest" / "main.toml"
        manuals: dict[str, Manual] = {}
        if manifest_manual_path.exists():
            for man_path in manifest_manual_path.parent.iterdir():
                manual_path = man_path / "man.yaml"
                if not manual_path.exists():
                    continue

                with manual_path.open("r") as source:
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

                manual_name = man_path.name
                manuals[manual_name] = Manual(
                    name=manual_name,
                    actions=actions,
                    dependencies=config.get("depends", []),
                )

        for man in self._get_order(manuals):
            self._apply(path / "manifest" / man, manuals[man])

        for page in manifest.pages:
            print(f"[INFO]: Building page '{page.name}'")
            manifest_path = self._resolve_location(path, page.location)
            self._build_subtree(manifest_path)

    @classmethod
    def _get_order(cls, mans: dict[str, Manual]) -> list[str]:
        if len(mans) == 0:
            return []

        graph: dict[str, set[str]] = {}
        possible_entrypoints = []
        for node in mans.values():
            deps = set()
            for dep in node.dependencies:
                if dep not in mans:
                    raise ValueError(
                        f"Unable to find dependency {dep} in manual {node.name}"
                    )
                deps.add(dep)
            graph[node.name] = deps
            if len(deps) == 0:
                possible_entrypoints.append(node.name)

        if len(possible_entrypoints) == 0:
            raise ValueError("Unable to find entrypoint manual")

        entrypoint = possible_entrypoints[0]

        current_order = [entrypoint]
        to_build = deque(list(set(graph.keys()) - {entrypoint}))
        while to_build:
            man = to_build.popleft()

            extra = graph[man] - set(current_order)
            if len(extra) == 0:
                current_order.append(man)
            else:
                to_build.append(man)

        return current_order

    def _resolve_location(self, cwd: Path, loc: str) -> Path:
        assert "@" in loc
        prefix, suffix = loc.split("@", maxsplit=1)
        match prefix:
            case "path":
                result = Path(suffix)
                if not result.is_absolute():
                    result = cwd / result
                return result.resolve()
            case "git":
                return self._clone_repository(suffix)
            case _:
                raise ValueError(f"Unknown prefix: {prefix}")

    def _apply(self, cwd: Path, manual: Manual):
        shell = Shell(cwd=cwd)
        for action in manual.actions:
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

        selector = ""
        if url.count("@") == 1:
            selector = url.split("@")[1]
            if selector.count("=") != 1:
                log_exception(f"Invalid repository selector: {selector} in {url}")
            selector_name, selector_value = selector.split("=")
            match selector_name:
                case "branch":
                    pass
                case "tag":
                    pass
                case "commit":
                    pass
                case _:
                    log_exception(
                        f"Unknown repository selector: {selector_name} in {url}"
                    )

        print(f"[INFO]: Cloning repository: {url}")
        user_name, user_repo = (
            url.removesuffix("@" + selector).removesuffix(".git").split("/")[-2:]
        )
        to_path = CACHE_DIR / user_name / user_repo
        if not to_path.exists():
            repo = Repo.clone_from(url, to_path)
        repo = Repo(to_path)
        repo.remotes.origin.pull()
        return to_path
