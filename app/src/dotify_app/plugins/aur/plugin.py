from dotify_lib.plugin import DotifyPlugin

from dotify_app.plugins.aur.procedures import (
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
