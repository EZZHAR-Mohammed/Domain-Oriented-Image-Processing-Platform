from domains.medical_domain import MedicalDomain
from domains.military_domain import MilitaryDomain
from domains.biology_domain import BiologyDomain
from domains.satellite_domain import SatelliteDomain
from domains.general_domain import GeneralDomain

class DomainManager:
    def __init__(self):
        self.domains = {
            "Santé": MedicalDomain(),
            "Militaire": MilitaryDomain(),
            "Biologie": BiologyDomain(),
            "Satellite": SatelliteDomain(),
            "Général": GeneralDomain(),
        }
        self.current_domain_key = None
        self.current_domain = None

    def set_domain(self, name):
        if name in self.domains:
            self.current_domain_key = name
            self.current_domain = self.domains[name]
            return True
        return False

    def get_current_filters(self):
        if self.current_domain is None:
            return []
        return self.current_domain.get_filters()

    def get_domain_names(self):
        return list(self.domains.keys())

    def get_current_domain_name(self):
        return self.current_domain_key