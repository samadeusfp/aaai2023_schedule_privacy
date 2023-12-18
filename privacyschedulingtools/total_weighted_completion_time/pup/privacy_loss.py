import math
from collections import defaultdict
from typing import List, Dict

from numpy import mean
from privacyschedulingtools.total_weighted_completion_time.entity.schedule import Schedule


def exact_match(schedule: Schedule, candidates: list):
    ''' The exact-match privacy loss for the given schedule and the candidates.'''
    if (len(candidates) == 0):
        return 0
    if (schedule not in candidates):
        return 0
    else:
        return 1 / len(candidates)


def distance_based_from_result_list(schedule: Schedule, result_list, normalize = "random"):

    if not normalize in ("random", "prior"):
        raise ValueError("Parameter normalize only allows values 'random' and 'prior'.")
    if sum(len(res['solutions']) for res in result_list) == 0:
        return [0] * len(schedule.jobs)

    true_weights = [j.weight for j in schedule.jobs.values()]

    per_item_loss = []
    for job in range(len(schedule.jobs)):
        i_occurences = defaultdict(int)
        for res in result_list:
            for candidate in res['solutions']:
                i_occurences[candidate[job]] += res['count']
        if sum(i_occurences.values()) == 0:
            d = 0
        else:
            d = sum([abs(true_weights[job] - w) * occ for w, occ in i_occurences.items()]) / sum(i_occurences.values())

        if normalize == "random":
            d_norm = _expected_distance_set(true_weights[job], schedule.params.weight_domain.get_all())
        else:
            d_norm = _expected_distance_distr(true_weights[job], schedule.params.get_weight_distribution_prior()[job])

        per_item_loss.append(1 - (d / d_norm))

    return per_item_loss


def distance_based(schedule: Schedule, candidates, normalize = "random", subtract=False):

    if not normalize in ("random", "prior"):
        raise ValueError("Parameter normalize only allows values 'random' and 'prior'.")
    if (len(candidates) == 0):
        return [0] * len(schedule.jobs)

    true_weights = [j.weight for j in schedule.jobs.values()]

    per_item_loss = []
    for job in range(len(schedule.jobs)):
        job_candidates = [c[job] for c in candidates]
        d = _expected_distance_set(true_weights[job], job_candidates)
        if normalize == "random":
            d_norm = _expected_distance_set(true_weights[job], schedule.params.weight_domain.get_all())
        else:
            d_norm = _expected_distance_distr(true_weights[job], schedule.params.get_weight_distribution_prior()[job])

        if subtract:
            per_item_loss.append(d_norm - d) #/ (schedule.params.weight_domain.get_max() - schedule.params.weight_domain.get_min())
        else:
            per_item_loss.append(1 - (d / d_norm))

    return per_item_loss


def _expected_distance_set(true_value: float, candidates: List[int]):
    '''Calculates the average/expected distance from the true value for a multi-set of candidate values.'''
    distances = [abs(true_value - c) for c in candidates]
    return mean(distances)


def _expected_distance_distr(true_value: float, candidates: Dict[int, float]):
    '''Calculates the average/expected distance from the true value for a probability distribution over the domain.'''
    if not math.isclose(1.0, sum(candidates.values())):
        raise ValueError(f"Candidates argument does not seem to represent a probability distribution. (Sum of probabilities: {sum(candidates.values())})")
    distances = [abs(true_value - c) * prob for c, prob in candidates.items()]
    return sum(distances)
