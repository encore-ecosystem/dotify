from abc import ABC
from dataclasses import dataclass

from dotify_lib.plugin.procedure import PluginProcedure


@dataclass
class DotifyPlugin(ABC):
    name: str
    procedures: dict[str, type[PluginProcedure]]
