from dotify_lib.logger import log_error, log_info
from dotify_lib.namespace import Namespace
from dotify_lib.plugin.procedure import PluginProcedure
from dotify_lib.shell import Shell
from pydantic import Field


class PacmanInstall(PluginProcedure):
    packages: list[str]
    num_retries: int = Field(default=3, ge=1)
    privileged: bool = True

    def run(self, shell: Shell, namespace: Namespace):
        command = f"pacman -S {' '.join(self.packages)} --noconfirm --needed"
        for retry in range(self.num_retries):
            log_info(f"Retry {retry + 1}/{self.num_retries}")
            if shell.run(command, privileged=self.privileged) == 0:
                break
            log_error(f"Failed to install package(s): {self.packages}")
