from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.plugin.builtin import DotifyPlugin_shell

from dataclasses import dataclass, field


@dataclass
class PluginManager:
    plugins: list[DotifyPlugin]

    @classmethod
    def default(cls) -> "PluginManager":
        return cls(plugins=[DotifyPlugin_shell()])
