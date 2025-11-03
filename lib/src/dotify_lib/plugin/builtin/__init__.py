from dotify_lib.plugin.builtin.git import DotifyPlugin_git
from dotify_lib.plugin.builtin.os import DotifyPlugin_os
from dotify_lib.plugin.builtin.pacman import DotifyPlugin_pacman
from dotify_lib.plugin.builtin.paru import DotifyPlugin_paru
from dotify_lib.plugin.builtin.shell import DotifyPlugin_shell

__all__ = [
    "DotifyPlugin_shell",
    "DotifyPlugin_pacman",
    "DotifyPlugin_git",
    "DotifyPlugin_paru",
    "DotifyPlugin_os",
]
