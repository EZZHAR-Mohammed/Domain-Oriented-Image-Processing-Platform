# domains/base_domain.py
from abc import ABC, abstractmethod
from typing import List


class BaseDomain(ABC):
    """Classe de base pour tous les domaines d'application"""

    def __init__(self):
        self.name: str = "Domaine de base"
        self.description: str = ""
        self.filters: List = []  # sera rempli par les sous-classes

    def get_filters(self) -> List:
        return self.filters

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description