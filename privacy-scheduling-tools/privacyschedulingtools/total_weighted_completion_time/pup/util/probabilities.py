from collections import defaultdict, namedtuple

import scipy
from privacyschedulingtools.total_weighted_completion_time.entity.domain import IntegerDomain

#TODO Tests
def calc_weight_distribution_prior(job_count: int, processing_time_domain: IntegerDomain, weight_domain: IntegerDomain):

    PJob = namedtuple("PJob", "w pt")
    possible_jobs = [PJob(w=w, pt=pt) for w in weight_domain.get_all() for pt in processing_time_domain.get_all()]
    # TODO this should be equal to the actual schedule optimization
    # we assume here that there is a strict total order on the jobs,
    # i.e. two jobs with the same w/pt-ratio will always appear in the same order in an optimized schedule
    # this simplifies the calculation of n_optimal_schedules and avoids counting duplicates in the permutations below
    possible_jobs.sort(key=lambda pjob: pjob.w/pjob.pt, reverse=True)

    # Combination with Repetition
    n_optimal_schedules = scipy.special.comb((len(possible_jobs) + job_count) - 1, job_count, exact=True)

    # dict of dicts (job -> weight -> permutations)
    distribution_dict = defaultdict(lambda: defaultdict(int))
    for index, job in enumerate(possible_jobs):
        n_jobs_higher_ratio = index + 1
        n_jobs_lower_ratio = len(possible_jobs) - index

        for job_in_schedule in range(job_count):

            n_jobs_earlier = job_in_schedule
            permutations_earlier = scipy.special.comb((n_jobs_higher_ratio + n_jobs_earlier) - 1, n_jobs_earlier, exact=True)

            n_jobs_later = job_count - (job_in_schedule + 1)
            permutations_later = scipy.special.comb((n_jobs_lower_ratio + n_jobs_later) - 1, n_jobs_later, exact=True)

            permutations_total = permutations_earlier * permutations_later
            distribution_dict[job_in_schedule][job.w] += permutations_total / n_optimal_schedules

    return distribution_dict

