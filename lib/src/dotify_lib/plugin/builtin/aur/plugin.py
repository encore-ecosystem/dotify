from dotify_lib.plugin.plugin import DotifyPlugin

from .procedures import (
    AurInstall,
    AurRemove,
    AurUpdate,
)


class Plugin_aur(DotifyPlugin):
    def __init__(self):
        super().__init__(
            name="aur",
            procedures={
                "install": AurInstall,
                "remove": AurRemove,
                "update": AurUpdate,
            },
        )
