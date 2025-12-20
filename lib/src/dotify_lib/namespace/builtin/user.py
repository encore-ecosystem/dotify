from pathlib import Path

from dotify_lib.namespace.namespace import Namespace


class NamespaceUser(Namespace):
    @property
    def home(self) -> Path:
        return Path().home()

    @property
    def config(self) -> Path:
        return self.home / ".config"

    @property
    def name(self) -> str:
        return self.home.name

    def get_fields(self) -> dict[str, object]:
        return {"home": self.home, "config": self.config, "name": self.name}
