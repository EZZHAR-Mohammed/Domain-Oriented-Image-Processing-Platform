# domains/biology_domain.py
from domains.base_domain import BaseDomain
from filters.enhancement.stain_enhancement import StainEnhancement
from filters.morphology.erosion import Erosion
from filters.morphology.cell_segmentation import CellSegmentation


class BiologyDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.name = "Biologie"
        self.description = "Adapté à la microscopie, coloration, segmentation cellulaire"
        self.filters = [
            StainEnhancement(),
            Erosion(),
            CellSegmentation(),
        ]