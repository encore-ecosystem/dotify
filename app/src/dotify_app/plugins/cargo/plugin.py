from dotify_lib.plugin.plugin import DotifyPlugin

from dotify_app.plugins.cargo.procedure import CargoInstall


class Plugin_cargo(DotifyPlugin):
    def __init__(self):
        super().__init__(
            name="cargo",
            procedures={
                "install": CargoInstall,
            },
        )
