import logging
import redbeat
from celery.schedules import crontab
from redbeat.schedulers import RedBeatConfig, RedBeatScheduler
import main
from utils.get_nested_value import get_nested_value
from redbeat import RedBeatSchedulerEntry

logger = logging.getLogger('agent_logger')


def check_and_update_cron(data):
    cron_value = get_nested_value(data, 'data', 'backup', 'cron')
    generated_id = get_nested_value(data, 'generatedId')
    dbms = get_nested_value(data, 'dbms')

    task_name = f'periodic.backup_{generated_id}'
    format_task_name = f"redbeat:{task_name}"
    task = "tasks.backup.periodic_backup"
    schedule = get_schedules()
    logger.info(f'crontab schedule: {schedule}')

    if cron_value is None:
        if format_task_name in schedule:
            remove_periodic_tasks([format_task_name])
            logger.info(f'Periodic task: {task_name} removed successfully')
            return False
        return False

    crontab_parts = cron_value.split() if cron_value else ["*", "*", "*", "*", "*"]
    crontab_schedule = get_crontab_object(crontab_parts)

    payload = {
        "generatedId": generated_id,
        "dbms": dbms,
    }
    if format_task_name in schedule:
        logger.info(f"Task '{format_task_name}' exists")
        actual_cron = get_crontab_as_array(schedule[format_task_name])
        if not compare_cron_arrays(actual_cron, crontab_parts):
            new_cron = get_crontab_object(crontab_parts)

            update_periodic_task(task_name, task, new_cron, (payload,))

    else:
        add_task(task_name, task, crontab_schedule, (payload,))
        logger.info(f"Periodic task '{task_name}' created successfully")


def add_task(name, task, schedule, args):
    entry = RedBeatSchedulerEntry(name, task, schedule, args=args, kwargs=None, app=main.app)
    entry.save()


def update_periodic_task(task_name, task, crontab_schedule, args):
    try:
        add_task(task_name, task, crontab_schedule, args)
        logger.info(f"Periodic task '{task_name}' updated successfully")
    except Exception as e:
        print(e)
        logger.info(e)


def get_schedules() -> dict:
    config = RedBeatConfig(main.app)
    schedule_key = config.schedule_key
    redis = redbeat.schedulers.get_redis(main.app)
    elements = redis.zrange(schedule_key, 0, -1, withscores=False)
    entries = {el: RedBeatSchedulerEntry.from_key(key=el, app=main.app) for el in elements}
    return entries


def get_crontab_as_array(entry):
    crontab_schedule = entry.schedule
    return [
        crontab_schedule._orig_minute,
        crontab_schedule._orig_hour,
        crontab_schedule._orig_day_of_month,
        crontab_schedule._orig_month_of_year,
        crontab_schedule._orig_day_of_week,
    ]


def get_crontab_object(array_entry):
    return crontab(minute=array_entry[0], hour=array_entry[1], day_of_week=array_entry[2], day_of_month=array_entry[3],
                   month_of_year=array_entry[4])


def compare_cron_arrays(cron1, cron2):
    return cron1 == cron2


def remove_periodic_tasks(task_names: list[str]):
    redbeat_scheduler = RedBeatScheduler(app=main.app)

    for task in task_names:
        entry = redbeat_scheduler.Entry.from_key(key=task, app=main.app)
        entry.delete()
