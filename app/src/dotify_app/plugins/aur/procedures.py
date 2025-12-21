from typing import Literal, Optional

from dotify_lib.logger import log_error, log_info
from dotify_lib.namespace import Namespace
from dotify_lib.plugin.procedure import PluginProcedure
from dotify_lib.shell import Shell
from pydantic import Field


class AurInstall(PluginProcedure):
    provider: Literal["yay", "paru"] = "yay"
    packages: list[str]
    num_retries: int = Field(default=3, ge=1)

    def run(self, shell: Shell, namespace: Namespace):
        command = f"{self.provider} -S {' '.join(self.packages)} --needed"
        for retry in range(self.num_retries):
            log_info(f"Retry {retry + 1}/{self.num_retries}")
            if shell.run(command) == 0:
                break
            log_error(f"Failed to install package(s): {self.packages}")


class AurRemove(PluginProcedure):
    provider: Literal["yay", "paru"] = "yay"
    packages: list[str]
    num_retries: int = Field(default=3, ge=1)

    def run(self, shell: Shell, namespace: Namespace):
        command = f"{self.provider} -R {' '.join(self.packages)}"
        for retry in range(self.num_retries):
            log_info(f"Retry {retry + 1}/{self.num_retries}")
            if shell.run(command) == 0:
                break
            log_error(f"Failed to remove package(s): {self.packages}")


class AurUpdate(PluginProcedure):
    provider: Literal["yay", "paru"] = "yay"
    privileged: Optional[bool] = None
    num_retries: int = Field(default=3, ge=1)

    def run(self, shell: Shell, namespace: Namespace):
        command = f"{self.provider} -Syu"
        for retry in range(self.num_retries):
            log_info(f"Retry {retry + 1}/{self.num_retries}")
            if shell.run(command) == 0:
                break
            log_error("Failed to update system")
