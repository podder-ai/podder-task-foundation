from abc import ABCMeta, abstractmethod
from pathlib import Path


class BaseConfigParser(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        return ""

    @classmethod
    @abstractmethod
    def detect_target(cls, file: Path) -> bool:
        return False

    @classmethod
    @abstractmethod
    def parse(cls, file: Path, encoding: str = "utf-8") -> dict:
        return {}
