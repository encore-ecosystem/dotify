from dotify_lib.plugin.plugin import DotifyPlugin
from dataclasses import dataclass


@dataclass
class DotifyPlugin_paru(DotifyPlugin):
    name: str = "paru"

    def hook_install(self, *args, **kwargss): ...
