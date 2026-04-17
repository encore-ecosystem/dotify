from dataclasses import dataclass, field
from pathlib import Path

from dotify_lib.namespace import Namespace
from dotify_lib.plugin import builtin
from dotify_lib.plugin.plugin import DotifyPlugin

BULTIN_PLUGINS = [
    builtin.Plugin_aur,
    builtin.Plugin_cargo,
    builtin.Plugin_git,
    builtin.Plugin_os,
    builtin.Plugin_pacman,
    builtin.Plugin_shell,
]


@dataclass
class PluginManager:
    plugins: dict[str, DotifyPlugin] = field(default_factory=dict)

    @classmethod
    def with_builtin_plugins(cls) -> "PluginManager":
        result = PluginManager()
        for plugin in BULTIN_PLUGINS:
            result.append(plugin())
        return result

    def append(self, plugin: DotifyPlugin):
        if plugin.name in self.plugins:
            print(f"[ERROR!]: Plugin {plugin.name} already appended!")
        self.plugins[plugin.name] = plugin

    def run_action(self, action: dict, namespace: Namespace, cwd: Path):
        procedure = action["procedure"]
        if "." not in procedure:
            print("[ERROR]: Plugin and hook should be splitted using '.'")
            exit(-1)

        plugin_name, hook_name = procedure.split(".")
        if plugin_name not in self.plugins:
            print(f"[ERROR]: Plugin '{plugin_name}' is unknown ")
            exit(-1)
        plugin = self.plugins[plugin_name]

        if "info" in action:
            print(f"[INFO]: {action['info']}")

        hook_callback_name = f"hook_{hook_name}"
        if (callback := getattr(plugin, hook_callback_name, None)) is None:
            print(f"[ERROR]: Plugin '{plugin_name}' does not have hook: {hook_name}")
            exit(-1)

        assert callback
        callback(**action, namespace=namespace, cwd=cwd)
