from abc import ABC, abstractmethod

from pydantic import BaseModel

from dotify_lib.namespace import Namespace
from dotify_lib.shell import Shell


class PluginProcedure(BaseModel, ABC):
    @abstractmethod
    def run(self, shell: Shell, namespace: Namespace):
        raise NotImplementedError
