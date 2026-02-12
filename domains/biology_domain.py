# domains/biology_domain.py
from domains.base_domain import BaseDomain
from filters.morphology.erosion import Erosion
from filters.enhancement.stain_enhancement import StainEnhancement
from filters.morphology.cell_segmentation import CellSegmentation
from filters.biology.cell_counting import CellCounting
from filters.advanced.super_resolution import SuperResolution

class BiologyDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.filters = [
            Erosion(),
            StainEnhancement(),
            CellSegmentation(),
            CellCounting(),       # Nouveau
            SuperResolution(),    # Nouveau
        ]