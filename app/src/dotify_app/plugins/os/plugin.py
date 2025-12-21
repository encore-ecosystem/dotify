from dotify_lib.plugin.plugin import DotifyPlugin

from dotify_app.plugins.os.procedures import (
    OsCopy,
    OsMkdir,
    OsMove,
    OsRemove,
    OsSymlink,
)


class Plugin_os(DotifyPlugin):
    def __init__(self):
        super().__init__(
            name="os",
            procedures={
                "move": OsMove,
                "symlink": OsSymlink,
                "copy": OsCopy,
                "mkdir": OsMkdir,
                "remove": OsRemove,
            },
        )
