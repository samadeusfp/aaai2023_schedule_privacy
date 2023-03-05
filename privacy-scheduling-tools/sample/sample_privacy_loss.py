from privacyschedulingtools.total_weighted_completion_time.entity.adversary.adversary import WSPTAdversary
from privacyschedulingtools.total_weighted_completion_time.entity.domain import IntegerDomain
from privacyschedulingtools.total_weighted_completion_time.entity.schedule import ScheduleFactory
from privacyschedulingtools.total_weighted_completion_time.entity.scheduling_parameters import SchedulingParameters
from privacyschedulingtools.total_weighted_completion_time.pup.privacy_loss import distance_based as distance_based_privacy_loss

# Set the settings for the scheduling problem
params = SchedulingParameters(
    job_count=10,
    processing_time_domain=IntegerDomain(min_value=15, max_value=30),
    weight_domain=IntegerDomain(min_value=1, max_value=5)
)

#Generate a random schedule for the scheduling problem
schedule_factory = ScheduleFactory(params)
schedule = schedule_factory.generate_random_optimized_schedule()

#Returns Schedules as list. Elements are structured as (job_count, processing_time, weight
print(schedule)
print("\n")

#Sets up the adversary
adversary = WSPTAdversary(params)

#Performs Inverse Scheduling Attack on Schedule
attack_result = adversary.execute_attack(schedule)
print(attack_result)

#Calculate Privacy Loss for every Job
privacy_loss = distance_based_privacy_loss(schedule,attack_result["solutions"],"random")
print(privacy_loss)

#Total Privacy Loss
print(max(privacy_loss))