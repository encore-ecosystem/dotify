from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class Shell:
    cwd: Path

    def run(self, cmd: str, privileged: bool = False) -> int:
        cmd = cmd.strip()
        cmd = ("sudo " if privileged else "") + cmd
        if cmd.startswith("cd "):
            path = cmd.split(" ", 1)[1].strip()
            self.cwd = (self.cwd / path).resolve()
            return 0
        else:
            result = subprocess.run(cmd, shell=True, cwd=self.cwd)
            return result.returncode
