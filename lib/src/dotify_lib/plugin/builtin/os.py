from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.utils.path import get_absolute_path
from dotify_lib.template import resolve
from dotify_lib.namespace import Namespace
from dotify_lib.shell import Shell
from dataclasses import dataclass
from pathlib import Path

import shutil
import os


@dataclass
class DotifyPlugin_os(DotifyPlugin):
    name: str = "os"

    def hook_symlink(
        self,
        cwd: Path,
        namespace: Namespace,
        *args,
        **kwargs,
    ):
        if "src" not in kwargs:
            print(f"[ERROR]: Provide src for os.symlink!")
            exit(-1)

        if "dst" not in kwargs:
            print(f"[ERROR]: Provide dst for os.symlink!")
            exit(-1)

        src = get_absolute_path(cwd, Path(resolve(kwargs["src"], namespace)))
        dst = get_absolute_path(cwd, Path(resolve(kwargs["dst"], namespace)))

        if not src.exists():
            print(f"[ERROR]: Source path {src} doesn't exists")
            exit(-1)
        dst.parent.mkdir(parents=True, exist_ok=True)

        print(f"[INFO]: Symlink {src} -> {dst}")
        shell = Shell(cwd=cwd)
        shell.run(
            cmd=f"ln -sf {src} {dst}",
            privileged=kwargs.get("privileged", False),
        )

    def hook_move(
        self,
        cwd: Path,
        namespace: Namespace,
        *args,
        **kwargs,
    ):
        if "src" not in kwargs:
            print(f"[ERROR]: Provide src for os.move!")
            exit(-1)

        if "dst" not in kwargs:
            print(f"[ERROR]: Provide dst for os.move!")
            exit(-1)

        src = get_absolute_path(cwd, Path(resolve(kwargs["src"], namespace)))
        dst = get_absolute_path(cwd, Path(resolve(kwargs["dst"], namespace)))

        if not src.exists():
            print(f"[ERROR]: Source path {src} doesn't exists")
            exit(-1)
        dst.parent.mkdir(parents=True, exist_ok=True)

        print(f"[INFO]: Move {src} -> {dst}")
        shell = Shell(cwd=cwd)
        shell.run(
            cmd=f"mv {src} {dst}",
            privileged=kwargs.get("privileged", False),
        )
