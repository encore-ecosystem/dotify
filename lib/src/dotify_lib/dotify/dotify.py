from dataclasses import dataclass

from dotify_lib.plugin import PluginManager
from pathlib import Path

import yaml


@dataclass
class Dotify:
    plugins: PluginManager

    def apply_from(self, path: Path):
        # add builtin plugins
        dotify_project_root = (
            Path(__file__).resolve().parent.parent.parent.parent.parent
        )
        plugins_path = dotify_project_root / "plugins"
        for plugin_path in plugins_path.glob("*"):
            self._apply(plugin_path)

    def _apply(self, path: Path):
        config_manifest_path = path / "dotify.toml"
        manifests_path = path / "manifests"
        if (
            config_manifest_path.exists()
            and manifests_path.exists()
            and manifests_path.is_dir()
        ):
            return self._apply_from_manifests(manifests_path)

        return self._apply_from_yaml(path / "main.yaml")

    def _apply_from_manifests(self, path: Path):
        return self._apply_from_yaml(path / "main.yaml")

    def _apply_from_yaml(self, path2yaml: Path):
        if not path2yaml.exists():
            print(f"[ERROR]: Unable to find `dotify.toml` or manifests dir in {path}")
            exit(-1)

        with path2yaml.open("r") as source:
            config = yaml.safe_load(source)
            if not config:
                config = {}

        # priority 1: plugin section
        if "plugin" in config:
            print(f"[INFO]: Loading 'plugin' section for {path2yaml}")
        # priority 2: dependencies section

        # priority 3: actions sections

        # print(path2yaml, config)
