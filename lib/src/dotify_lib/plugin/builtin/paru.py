from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.namespace import Namespace
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DotifyPlugin_paru(DotifyPlugin):
    name: str = "paru"

    def hook_install(self, cwd: Path, namespace: Namespace, *args, **kwargss):
        raise NotImplementedError
