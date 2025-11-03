from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.shell import Shell
from dotify_lib.namespace import Namespace
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DotifyPlugin_pacman(DotifyPlugin):
    name: str = "pacman"

    def hook_install(
        self,
        cwd: Path,
        namespace: Namespace,
        *args,
        **kwargs,
    ):
        if "package" not in kwargs:
            print(f"[ERROR]: pacman required `package` argument!")
            exit(-1)
        shell = Shell(cwd)
        command = f"pacman -S {' '.join(kwargs['package'])} --noconfirm --needed"
        status = shell.run(command, privileged=True)
        if status != 0:
            print(f"Failed to install package: {kwargs['package']}")
            exit(-1)
