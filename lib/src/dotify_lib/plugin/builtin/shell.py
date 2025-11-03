from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.namespace import Namespace
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DotifyPlugin_shell(DotifyPlugin):
    name: str = "shell"

    def hook_run(self, cwd: Path, namespace: Namespace, *args, **kwargs):
        raise NotImplementedError
