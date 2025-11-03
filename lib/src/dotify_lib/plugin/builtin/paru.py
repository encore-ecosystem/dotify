from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.namespace import Namespace
from dotify_lib.shell import Shell
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DotifyPlugin_paru(DotifyPlugin):
    name: str = "paru"

    def hook_install(self, cwd: Path, namespace: Namespace, *args, **kwargs):
        if "package" not in kwargs:
            print(f"[ERROR]: paru required `package` argument!")
            exit(-1)
        shell = Shell(cwd)
        command = f"paru -S {' '.join(kwargs['package'])} --noconfirm --needed"
        status = shell.run(command, privileged=False)
        if status != 0:
            print(f"Failed to install package: {kwargs['package']}")
            exit(-1)
