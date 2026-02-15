# domains/military_domain.py
from domains.base_domain import BaseDomain
from filters.edge_detection.canny import CannyEdge
from filters.enhancement.thermal_enhancement import ThermalEnhancement
from filters.morphology.object_detection import ObjectDetection
from filters.military.target_detection import TargetDetection
from filters.advanced.anomaly_detection import AnomalyDetection

class MilitaryDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.filters = [
            CannyEdge(),
            ThermalEnhancement(),
            ObjectDetection(),
            TargetDetection(),    # Nouveau
            AnomalyDetection(),   # Nouveau
        ]