# domains/biology_domain.py
from domains.base_domain import BaseDomain
from filters.morphology.erosion import Erosion
from filters.enhancement.stain_enhancement import StainEnhancement
from filters.morphology.cell_segmentation import CellSegmentation
from filters.biology.cell_counting import CellCounting
from filters.advanced.unet_segmentation import UNet   


class BiologyDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.name = "Biologie"
        self.description = "Filtres pour microscopie et analyse cellulaire"
        self.filters = [
            Erosion(),
            StainEnhancement(),
            CellSegmentation(),
            CellCounting(),
            UNet(),  
        ]