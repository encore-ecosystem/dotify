from dotify_lib.logger import log_exception
from dotify_lib.namespace import Namespace
from dotify_lib.plugin.procedure import PluginProcedure
from dotify_lib.shell import Shell


class CargoInstall(PluginProcedure):
    package: str

    def run(self, shell: Shell, namespace: Namespace):
        cmd = f"cargo install {self.package}"
        if shell.run(cmd) != 0:
            log_exception(f"Failed to install package: {self.package}")
