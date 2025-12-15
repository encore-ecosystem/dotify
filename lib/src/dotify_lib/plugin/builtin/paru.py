from dataclasses import dataclass
from pathlib import Path

from dotify_lib.namespace import Namespace
from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.shell import Shell

DEFAULT_NUM_RETRIES = 3


@dataclass
class DotifyPlugin_paru(DotifyPlugin):
    name: str = "paru"

    def hook_install(self, cwd: Path, namespace: Namespace, *args, **kwargs):
        if "package" not in kwargs:
            print("[ERROR]: paru required `package` argument!")
            exit(-1)
        shell = Shell(cwd)

        for retry in range(kwargs.get("retries", DEFAULT_NUM_RETRIES)):
            print(f"[INFO]: Retry {retry}")
            noconfirm = "" if kwargs.get("manual", False) else "--noconfirm"
            needed = "" if kwargs.get("needed", True) else "--needed"
            command = f"paru -S {' '.join(kwargs['package'])} {noconfirm} {needed}"
            status = shell.run(command, privileged=False)
            if status != 0:
                print(f"[ERROR]: Failed to install package: {kwargs['package']}")
            else:
                break
        else:
            exit(-1)
