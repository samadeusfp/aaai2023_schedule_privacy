import typing
from dataclasses import dataclass
from enum import Enum

# the different outcomes for a search with the privacy threshold being based on the attack success probability
from privacyschedulingtools.total_weighted_completion_time.entity.schedule import Schedule


class Outcome(Enum):
    NOT_FOUND = 0
    SIZE_ZERO = 1
    TRUE_W_NOT_IN_SET = 2
    SOLUTION_COUNT_LARGE_ENOUGH = 3
    FOUND = 4


@dataclass
class Result:
    outcome: Outcome = None
    original_schedule: Schedule = None
    privatized_schedule: Schedule = None
    adversary_solution_count: int = None
    privacy_loss: float = None
    privacy_loss_per_job: typing.List = None
    utility_loss: float = None

