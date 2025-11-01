from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.shell import Shell
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DotifyPlugin_pacman(DotifyPlugin):
    name: str = "pacman"

    def hook_install(
        self,
        cwd: Path,
        *args,
        **kwargs,
    ):
        shell = Shell(cwd)
        command = f"pacman -S {' '.join(kwargs['package'])}"
        status = shell.run(command, privileged=True)
        if status != 0:
            print(f"Failed to install package: {kwargs['package']}")
            exit(-1)
