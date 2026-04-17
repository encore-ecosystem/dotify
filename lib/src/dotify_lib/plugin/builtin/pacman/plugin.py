from dotify_lib.plugin.plugin import DotifyPlugin

from .procedures import PacmanInstall


class Plugin_pacman(DotifyPlugin):
    def __init__(self):
        super().__init__(
            name="pacman",
            procedures={
                "install": PacmanInstall,
            },
        )
