# domains/general_domain.py
from domains.base_domain import BaseDomain
from filters.smoothing.gaussian_blur import GaussianBlur
from filters.edge_detection.canny import CannyEdge
from filters.enhancement.contrast_enhancement import ContrastEnhancement


class GeneralDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.name = "Général"
        self.description = "Filtres polyvalents pour tout type d'image"
        self.filters = [
            GaussianBlur(),
            CannyEdge(),
            ContrastEnhancement(),
        ]