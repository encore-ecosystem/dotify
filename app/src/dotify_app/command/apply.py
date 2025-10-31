from dotify_lib.plugin import PluginManager
from dotify_lib.manifest import DotifyProjectManifest
from dotify_lib.dotify import Dotify
from pathlib import Path


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
        print(f"[ERROR]: Unable to open manifest file")
        exit(-1)

    # step 1: initialize plugin manager
    plugin_manager = PluginManager.default()

    # step 2: apply config
    Dotify(plugin_manager).apply_from(cwd)
