# domains/military_domain.py
from domains.base_domain import BaseDomain
from filters.edge_detection.canny import CannyEdge
from filters.enhancement.thermal_enhancement import ThermalEnhancement
from filters.morphology.object_detection import ObjectDetection


class MilitaryDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.name = "Militaire"
        self.description = "Filtres pour reconnaissance, détection d'objets, imagerie thermique"
        self.filters = [
            CannyEdge(),
            ThermalEnhancement(),
            ObjectDetection(),
        ]