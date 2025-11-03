from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.shell import Shell
from dotify_lib.namespace import Namespace
from dataclasses import dataclass
from pathlib import Path

import shutil


@dataclass
class DotifyPlugin_git(DotifyPlugin):
    name: str = "git"

    def hook_clone(
        self,
        cwd: Path,
        namespace: Namespace,
        *args,
        **kwargs,
    ):
        if "url" not in kwargs:
            print(f"[ERROR]: Provide url for git.clone!")
            exit(-1)
        url: str = kwargs["url"]

        folder_name = url.removesuffix(".git").split("/")[-1]
        repo_path = cwd / folder_name
        if repo_path.exists():
            shutil.rmtree(repo_path)

        shell = Shell(cwd)
        status = shell.run(f"git clone {url}")
        if status != 0:
            print(f"Failed to clone repository: {url}")
            exit(-1)
