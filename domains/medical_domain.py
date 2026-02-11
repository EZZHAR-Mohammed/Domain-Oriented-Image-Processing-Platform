# domains/medical_domain.py
from domains.base_domain import BaseDomain
from filters.smoothing.gaussian_blur import GaussianBlur
from filters.enhancement.histogram_equalization import HistogramEqualization
from filters.enhancement.bone_enhancement import BoneEnhancement


class MedicalDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.name = "Santé"
        self.description = "Optimisé pour imagerie médicale (radiographie, IRM, etc.)"
        self.filters = [
            GaussianBlur(),
            HistogramEqualization(),
            BoneEnhancement(),
        ]