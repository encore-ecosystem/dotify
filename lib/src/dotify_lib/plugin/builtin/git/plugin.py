from dotify_lib.plugin.plugin import DotifyPlugin

from .procedures import GitClone


class Plugin_git(DotifyPlugin):
    def __init__(self):
        super().__init__(
            name="git",
            procedures={
                "clone": GitClone,
            },
        )
