from dotify_lib.plugin import DotifyPlugin

from dotify_app.plugins.package.procedures import (
    PackageInstall,
    PackageRemove,
    PackageUpdate,
)


class Plugin_package(DotifyPlugin):
    def __init__(self):
        super().__init__(
            name="package",
            procedures={
                "install": PackageInstall,
                "remove": PackageRemove,
                "update": PackageUpdate,
            },
        )
