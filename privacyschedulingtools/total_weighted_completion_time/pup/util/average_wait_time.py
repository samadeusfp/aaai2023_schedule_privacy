from privacyschedulingtools.total_weighted_completion_time.entity.schedule import Schedule


def calculate(schedule: Schedule) -> float:
    # average wait time is equal to average start time as all jobs are ready to be processed from the start
    current_time = 0
    wait_time_sum = 0
    for job_id in schedule.schedule_order:
        wait_time_sum += current_time
        current_time += schedule.jobs[job_id].processing_time
    return wait_time_sum/len(schedule.jobs)