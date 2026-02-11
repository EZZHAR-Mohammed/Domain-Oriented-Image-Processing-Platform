# domains/satellite_domain.py
from domains.base_domain import BaseDomain
from filters.enhancement.vegetation_index import VegetationIndex
from filters.smoothing.cloud_removal import CloudRemoval
from filters.enhancement.terrain_enhancement import TerrainEnhancement


class SatelliteDomain(BaseDomain):
    def __init__(self):
        super().__init__()
        self.name = "Satellite"
        self.description = "Traitement d'images satellites/aériennes (NDVI, nuages, terrain)"
        self.filters = [
            VegetationIndex(),
            CloudRemoval(),
            TerrainEnhancement(),
        ]