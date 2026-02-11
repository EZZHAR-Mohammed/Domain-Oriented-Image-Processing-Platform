# filters/base_filter.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import cv2


class BaseFilter(ABC):
    """
    Classe abstraite de base pour tous les filtres.
    Chaque filtre doit implémenter apply() et peut surcharger les autres méthodes.
    """

    def __init__(self):
        self.name: str = "Filtre inconnu"
        self.category: str = "Général"
        self.description: str = "Description non fournie"

    @abstractmethod
    def apply(self, image: cv2.Mat, params: Dict[str, Any]) -> cv2.Mat:
        """Applique le filtre et retourne l'image traitée"""
        pass

    def get_default_params(self) -> Dict[str, Any]:
        """Paramètres par défaut (à surcharger si besoin)"""
        return {}

    def get_ui_controls(self, parent=None) -> Optional['QWidget']:
        """
        Retourne un widget Qt pour régler les paramètres (sliders, etc.)
        Retourne None si pas d'interface personnalisée
        """
        return None

    def __str__(self) -> str:
        return self.name