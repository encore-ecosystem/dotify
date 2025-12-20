from pathlib import Path

from dotify_lib.logger import log_info
from dotify_lib.namespace import Namespace
from dotify_lib.path import get_absolute_path
from dotify_lib.plugin.procedure import PluginProcedure
from dotify_lib.resolve import resolve
from dotify_lib.shell import Shell


class OsMove(PluginProcedure):
    src_patterns: list[str]
    dst: str
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        log_info(f"Moving {self.src_patterns} -> {self.dst}")
        shell.run(
            cmd=f"mv {' '.join(self.src_patterns)} {self.dst}",
            privileged=self.privileged,
        )


class OsCopy(PluginProcedure):
    src_patterns: list[str]
    dst: str
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        log_info(f"Copying {self.src_patterns} -> {self.dst}")
        shell.run(
            cmd=f"cp {' '.join(self.src_patterns)} {self.dst}",
            privileged=self.privileged,
        )


class OsSymlink(PluginProcedure):
    src: str
    dst: str
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        src = get_absolute_path(shell.cwd, Path(resolve(self.src, namespace)))
        dst = get_absolute_path(shell.cwd, Path(resolve(self.dst, namespace)))

        log_info(f"Symlink {src} -> {dst}")
        shell.run(cmd=f"ln -sf {src} {dst}", privileged=self.privileged)


class OsMkdir(PluginProcedure):
    path: str
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        log_info(f"Creating directory {self.path}")
        shell.run(cmd=f"mkdir -p {self.path}", privileged=self.privileged)
