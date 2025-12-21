from dotify_lib.logger import log_exception
from dotify_lib.namespace import Namespace
from dotify_lib.plugin.procedure import PluginProcedure
from dotify_lib.shell import Shell


class ShellRun(PluginProcedure):
    command: str
    args: list[str]
    privileged: bool = False

    def run(self, shell: Shell, namespace: Namespace):
        cmd = f"{self.command} {' '.join(self.args)}"
        status = shell.run(
            cmd=cmd,
            privileged=self.privileged,
        )
        if status != 0:
            log_exception(f"Something went wrong during executing this command: {cmd}")


class ShellPath(PluginProcedure):
    path: str

    def run(self, shell: Shell, namespace: Namespace):
        cmd = f"PATH=$PATH:{self.path}"
        if shell.run(cmd=cmd) != 0:
            log_exception(f"Something went wrong during executing this command: {cmd}")
