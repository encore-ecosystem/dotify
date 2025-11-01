from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.shell import Shell
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DotifyPlugin_git(DotifyPlugin):
    name: str = "git"

    def hook_clone(
        self,
        cwd: Path,
        *args,
        **kwargs,
    ):
        if "url" not in kwargs:
            print(f"[ERROR]: Provide url for git.clone!")
            exit(-1)
        url = kwargs["url"]

        shell = Shell(cwd)
        status = shell.run(f"git clone {url}")
        if status != 0:
            print(f"Failed to clone repository: {url}")
            exit(-1)
