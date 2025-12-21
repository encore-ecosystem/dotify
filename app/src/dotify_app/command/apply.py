from pathlib import Path

from dotify_lib.dotify import Dotify
from dotify_lib.manifest import DotifyProjectManifest
from dotify_lib.namespace import DotifyNamespace
from dotify_lib.plugin import PluginManager

from dotify_app.plugins.aur import Plugin_aur
from dotify_app.plugins.cargo import Plugin_cargo
from dotify_app.plugins.git import Plugin_git
from dotify_app.plugins.os import Plugin_os
from dotify_app.plugins.pacman import Plugin_pacman
from dotify_app.plugins.shell import Plugin_shell


def apply(*args):
    args = args[0]
    cwd = Path().resolve()

    # step 0: load dotify manifest
    manifest_path = cwd / "dotify.toml"
    if not manifest_path.exists():
        print(f"[ERROR]: Unable to find manifest in: {manifest_path}")
        exit(-1)

    manifest = DotifyProjectManifest.read(manifest_path)
    if manifest is None:
        print("[ERROR]: Unable to open manifest file")
        exit(-1)

    # step 1: initialize plugin manager
    plugin_manager = PluginManager()
    plugin_manager.append(Plugin_shell())
    plugin_manager.append(Plugin_os())
    plugin_manager.append(Plugin_aur())
    plugin_manager.append(Plugin_git())
    plugin_manager.append(Plugin_cargo())
    plugin_manager.append(Plugin_pacman())

    # step 2: apply config
    manifests_folder = cwd / "manifests"
    if manifests_folder_overide := args.manifest:
        manifests_folder_overide = Path(manifests_folder_overide)
        if manifests_folder_overide.is_absolute():
            manifests_folder = manifests_folder_overide
        else:
            manifests_folder = (cwd / manifests_folder_overide).resolve()

    Dotify(plugin_manager, DotifyNamespace()).apply(manifests_folder)
