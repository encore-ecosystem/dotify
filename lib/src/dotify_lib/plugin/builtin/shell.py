from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.namespace import Namespace
from dotify_lib.shell import Shell
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DotifyPlugin_shell(DotifyPlugin):
    name: str = "shell"

    def hook_run(self, cwd: Path, namespace: Namespace, *args, **kwargs):
        if "command" not in kwargs:
            print("[ERROR]: Please, provide `command` for shell.run!")
            exit(-1)

        shell = Shell(cwd=cwd)
        cmd = f"{kwargs['command']} {' '.join(kwargs.get('args', []))}"
        status = shell.run(
            cmd=cmd,
            privileged=kwargs.get("privileged", False),
        )
        if status != 0:
            print(f"[ERROR]: Something went wrong during executing this command: {cmd}")
            exit(-1)
