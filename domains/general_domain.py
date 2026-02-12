# domains/general_domain.py
from domains.base_domain import BaseDomain
from filters.smoothing.gaussian_blur import GaussianBlur
from filters.edge_detection.canny import CannyEdge
from filters.enhancement.contrast_enhancement import ContrastEnhancement
from filters.general.edge_sharpening import EdgeSharpening
from filters.advanced.super_resolution import SuperResolution

class GeneralDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.filters = [
            GaussianBlur(),
            CannyEdge(),
            ContrastEnhancement(),
            EdgeSharpening(),     # Nouveau
            SuperResolution(),    # Nouveau
        ]