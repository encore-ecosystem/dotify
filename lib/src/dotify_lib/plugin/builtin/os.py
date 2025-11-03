from dotify_lib.plugin.plugin import DotifyPlugin
from dotify_lib.utils.path import get_absolute_path
from dotify_lib.template import resolve
from dotify_lib.namespace import Namespace
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

        try:
            print(f"[INFO] {src} -> {dst}")
            os.symlink(src, dst)
        except FileExistsError:
            print(f"[WARN]: Symlink {dst} already exists")
