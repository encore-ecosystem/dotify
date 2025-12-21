from dotify_lib.plugin.plugin import DotifyPlugin

from dotify_app.plugins.shell.procedures import ShellPath, ShellRun


class Plugin_shell(DotifyPlugin):
    def __init__(self):
        super().__init__(name="shell", procedures={"run": ShellRun, "path": ShellPath})
