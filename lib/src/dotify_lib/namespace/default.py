from dataclasses import dataclass
from dotify_lib.namespace import Namespace
from dotify_lib.namespace.builtin import NamespaceUser


@dataclass
class DotifyNamespace(Namespace):
    user: NamespaceUser = NamespaceUser()
