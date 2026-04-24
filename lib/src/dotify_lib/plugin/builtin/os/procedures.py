from pathlib import Path

from dotify_lib.logger import log_exception, log_info, log_warning
from dotify_lib.namespace import Namespace
from dotify_lib.path import get_absolute_path
from dotify_lib.plugin.procedure import PluginProcedure
from dotify_lib.resolve import resolve
from dotify_lib.shell import Shell


class OsMove(PluginProcedure):
    src: list[str] | str
    dst: str
    skip_if_not_exists: bool = False
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        src_raw = self.src if isinstance(self.src, list) else [self.src]
        src_res = [
            get_absolute_path(shell.cwd, Path(resolve(src, namespace))).__str__()
            for src in src_raw
        ]
        dst = get_absolute_path(shell.cwd, Path(resolve(self.dst, namespace))).__str__()

        log_info(f"Moving {src_res} -> {dst}")
        shell.run(
            cmd=f"mv {' '.join(src_res)} {dst}",
            privileged=self.privileged,
        )


class OsCopy(PluginProcedure):
    src: list[str] | str
    dst: str
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        src_raw = self.src if isinstance(self.src, list) else [self.src]
        src_res = [
            get_absolute_path(shell.cwd, Path(resolve(src, namespace))).__str__()
            for src in src_raw
        ]
        dst = get_absolute_path(shell.cwd, Path(resolve(self.dst, namespace))).__str__()

        log_info(f"Copying {src_res} -> {dst}")
        status = shell.run(
            cmd=f"cp {' '.join(src_res)} {dst}",
            privileged=self.privileged,
        )
        if status != 0:
            log_exception(f"Failed to copy {src_res} to {dst}")


class OsSymlink(PluginProcedure):
    src: str
    dst: str
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        src = get_absolute_path(shell.cwd, Path(resolve(self.src, namespace)))
        dst = get_absolute_path(shell.cwd, Path(resolve(self.dst, namespace)))

        log_info(f"Symlink {src} -> {dst}")
        status = shell.run(cmd=f"ln -sf {src} {dst}", privileged=self.privileged)
        if status != 0:
            log_exception(f"Failed to create symlink {src} -> {dst}")


class OsMkdir(PluginProcedure):
    path: str
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        path = get_absolute_path(shell.cwd, Path(resolve(self.path, namespace)))
        log_info(f"Creating directory {path}")
        status = shell.run(cmd=f"mkdir -p {path}", privileged=self.privileged)
        if status != 0:
            log_exception(f"Failed to create directory {path}")


class OsRemove(PluginProcedure):
    src: list[str] | str
    not_exists_ok: bool = False
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        sources_raw = self.src if isinstance(self.src, list) else [self.src]
        sources_resolved = []
        for src in sources_raw:
            src = get_absolute_path(
                cwd=shell.cwd, path=Path(resolve(string=src, namespace=namespace))
            )
            if not src.exists():
                msg = f"Source {src} does not exist"
                (log_warning if not self.not_exists_ok else log_exception)(msg)
                continue
            sources_resolved.append(src.__str__())

        if len(sources_resolved) == 0:
            log_warning("No sources to remove")
            return

        log_info(f"Removing {sources_resolved}")
        status = shell.run(
            cmd=f"rm {' '.join(sources_resolved)}", privileged=self.privileged
        )
        if status != 0:
            log_exception(f"Failed to remove {sources_resolved}")
