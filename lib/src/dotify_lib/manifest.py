from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import tomllib


@dataclass
class DotifyProjectConfig:
    name: str = "unknown"
    description: str = ""
    version: str = "0.0.1"
    author: str = ""


@dataclass
class DotifyProjectManifest:
    config: DotifyProjectConfig

    @classmethod
    def default(cls) -> "DotifyProjectManifest":
        return cls(config=DotifyProjectConfig())

    @classmethod
    def read(cls, path: Path) -> Optional["DotifyProjectManifest"]:
        if not path.exists() or not path.is_file():
            return None

        with path.open("rb") as source:
            manifest_overides = tomllib.load(source)

        manifest = cls.default()

        if "config" in manifest_overides:
            if "name" in manifest_overides["config"]:
                manifest.config.name = manifest_overides["config"]["name"]
            if "version" in manifest_overides["config"]:
                manifest.config.version = manifest_overides["config"]["version"]

            # skip: description, author
            # because it is unused information for dotify

        return manifest
