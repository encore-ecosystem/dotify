import tomllib
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from dotify_lib.plugin.procedure import PluginProcedure


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Manual(StrictModel):
    name: str = Field(min_length=1)
    actions: list[PluginProcedure] = Field(default=[])
    dependencies: list[str] = Field(default=[])


class PresetSection(StrictModel):
    name: str = "unknown"
    description: str = ""
    version: str = "0.0.1"
    author: str = ""


class PageSection(StrictModel):
    name: str = Field(min_length=1)
    location: str = Field(min_length=1)


class ProjectManifest(StrictModel):
    preset: PresetSection
    pages: list[PageSection]

    @classmethod
    def get_default_filename(cls) -> str:
        return "dotify.toml"

    @classmethod
    def read(cls, path: Path) -> Optional["ProjectManifest"]:
        if not path.exists() or not path.is_file():
            return None

        with path.open("rb") as source:
            manifest_dict = tomllib.load(source)

        preset = PresetSection(**manifest_dict.get("preset", {}))
        pages = []
        page_section = manifest_dict.get("pages", {})
        for page_name in page_section:
            pages.append(PageSection(name=page_name, **page_section[page_name]))
        manifest = cls(
            preset=preset,
            pages=pages,
        )
        return manifest

    def __hash__(self) -> int:
        return hash(self.preset.name)
