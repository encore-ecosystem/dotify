from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.plugin.builtin import (
    DotifyPlugin_shell,
    DotifyPlugin_pacman,
    DotifyPlugin_git,
    DotifyPlugin_paru,
)

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PluginManager:
    plugins: dict[str, DotifyPlugin] = field(default_factory=dict)

    @classmethod
    def default(cls) -> "PluginManager":
        res = cls()
        res.append(DotifyPlugin_shell())
        res.append(DotifyPlugin_pacman())
        res.append(DotifyPlugin_git())
        res.append(DotifyPlugin_paru())
        return res

    def append(self, plugin: DotifyPlugin):
        if plugin.name in self.plugins:
            print(f"[ERROR!]: Plugin {plugin.name} already appended!")
        self.plugins[plugin.name] = plugin

    def run_action(self, action: dict, cwd: Path):
        procedure = action["procedure"]
        if "." not in procedure:
            print(f"[ERROR]: Plugin and hook should be splitted using '.'")
            exit(-1)

        plugin_name, hook_name = procedure.split(".")
        if plugin_name not in self.plugins:
            print(f"[ERROR]: Plugin '{plugin_name}' is unknown ")
            exit(-1)
        plugin = self.plugins[plugin_name]

        hook_callback_name = f"hook_{hook_name}"
        if (callback := getattr(plugin, hook_callback_name, None)) is None:
            print(f"[ERROR]: Plugin '{plugin_name}' does not have hook: {hook_name}")
            exit(-1)

        callback(**action, cwd=cwd)
