from privacyschedulingtools.total_weighted_completion_time.entity.schedule import Schedule


def calculate(schedule: Schedule) -> float:
    twct = 0
    current_time = 0
    for job_id in schedule.schedule_order:
        current_time += schedule.jobs[job_id].processing_time
        twct += current_time
    return twct
