# domains/medical_domain.py
from domains.base_domain import BaseDomain
from filters.smoothing.gaussian_blur import GaussianBlur
from filters.enhancement.histogram_equalization import HistogramEqualization
from filters.enhancement.bone_enhancement import BoneEnhancement
from filters.advanced.anomaly_detection import AnomalyDetection
from filters.medical.adaptive_denoising import AdaptiveDenoising
from filters.advanced.super_resolution import SuperResolution

class MedicalDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.filters = [
            GaussianBlur(),
            HistogramEqualization(),
            BoneEnhancement(),
            AdaptiveDenoising(),  # Nouveau
            AnomalyDetection(),   # Nouveau
            SuperResolution(),    # Nouveau
        ]