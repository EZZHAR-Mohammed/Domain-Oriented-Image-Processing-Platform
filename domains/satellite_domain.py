# domains/satellite_domain.py
from domains.base_domain import BaseDomain
from filters.enhancement.vegetation_index import VegetationIndex
from filters.smoothing.cloud_removal import CloudRemoval
from filters.enhancement.terrain_enhancement import TerrainEnhancement
from filters.satellite.cloud_detection import CloudDetection
from filters.advanced.super_resolution import SuperResolution

class SatelliteDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.filters = [
            VegetationIndex(),
            CloudRemoval(),
            TerrainEnhancement(),
            CloudDetection(),     # Nouveau
            SuperResolution(),    # Nouveau
        ]