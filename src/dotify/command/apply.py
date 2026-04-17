from pathlib import Path

from dotify_lib.dotify import Dotify
from dotify_lib.namespace import DotifyNamespace
from dotify_lib.plugin import PluginManager


def apply(*args):
    args = args[0]
    cwd = Path().resolve()
    plugin_manager = PluginManager.with_builtin_plugins()
    Dotify(plugin_manager, DotifyNamespace()).apply_manifest(cwd)
