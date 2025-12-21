from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict

from dotify_lib.namespace import Namespace
from dotify_lib.shell import Shell


class PluginProcedure(BaseModel, ABC):
    model_config = ConfigDict(extra="forbid")

    info: str | None = None
    skip_condition: str | None = None

    @abstractmethod
    def run(self, shell: Shell, namespace: Namespace):
        raise NotImplementedError
