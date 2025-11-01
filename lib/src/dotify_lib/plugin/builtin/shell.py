from dotify_lib.plugin.plugin import DotifyPlugin
from dataclasses import dataclass


@dataclass
class DotifyPlugin_shell(DotifyPlugin):
    name: str = "shell"

    def hook_run(self, *args, **kwargs): ...
