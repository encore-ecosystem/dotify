from .aur.plugin import Plugin_aur
from .cargo.plugin import Plugin_cargo
from .git.plugin import Plugin_git
from .os.plugin import Plugin_os
from .pacman.plugin import Plugin_pacman
from .shell.plugin import Plugin_shell

__all__ = [
    "Plugin_aur",
    "Plugin_cargo",
    "Plugin_git",
    "Plugin_os",
    "Plugin_pacman",
    "Plugin_shell",
]
