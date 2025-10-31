from abc import ABC, abstractclassmethod


class DotifyPlugin(ABC):
    hooks: list[str]
