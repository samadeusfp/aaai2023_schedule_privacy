from dataclasses import dataclass, field

from privacyschedulingtools.total_weighted_completion_time.entity.domain import Domain
from privacyschedulingtools.total_weighted_completion_time.pup.util.probabilities import calc_weight_distribution_prior


@dataclass
class SchedulingParameters:
    job_count: int
    processing_time_domain: Domain
    weight_domain: Domain
    weight_distribution_prior: dict = field(init=False)

    def get_weight_distribution_prior(self):
        if not hasattr(self, "weight_distribution_prior"):
            distr = calc_weight_distribution_prior(self.job_count, self.processing_time_domain, self.weight_domain)
            self.__setattr__('weight_distribution_prior', distr)
        return self.weight_distribution_prior