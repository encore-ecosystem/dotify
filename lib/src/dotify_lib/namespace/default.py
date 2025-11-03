from dataclasses import dataclass

from dotify_lib.namespace.builtin import NamespaceUser
from dotify_lib.namespace.namespace import Namespace


@dataclass
class DotifyNamespace(Namespace):
    user: NamespaceUser = NamespaceUser()
