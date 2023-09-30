from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from config.config import get_config
from utils.utils import get_main_logger, create_result, func_name
from pymongo import MongoClient

conf = get_config()
l = get_main_logger('job_manager')


print(f"{conf.get('db_url')}:{conf.get('db_port')}")
client = MongoClient(f"{conf.get('db_url')}:{conf.get('db_port')}",
                     username=conf.get('username'),
                     password=conf.get('password'),
                     authSource=conf.get('db_name'),
                     authMechanism='SCRAM-SHA-1')


def setup_scheduler():
    jobstores = {
        'default': MongoDBJobStore(database=conf.get('db_name'),
                                   client=client,
                                   collection='vaaas_ip_scanner_jobs',
                                   port=int(conf.get('db_port')))
    }
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    # sched = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults,timezone='Europe/Athens')
    sched = BackgroundScheduler(jobstores=jobstores, timezone='Europe/Athens')

    return sched
    # sched.start()


def get_all_jobs(scheduler: BackgroundScheduler):
    try:
        result = []
        for job in scheduler.get_jobs():
            job = {
                "id": job.id,
                "name": job.name,
                "args": job.args,
                "kwargs": job.kwargs,
                # "function": job.func, # pickled function is not serializable
                "function_ref": job.func_ref,
                "executor": job.executor,
                "next_run_time": str(job.next_run_time)
            }
            result.append(job)
        return create_result(items=result, result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def get_one_job(scheduler: BackgroundScheduler, job_id: str):
    try:
        assert job_id, Exception('Job ID was either null or empty')
        job = scheduler.get_job(job_id=job_id)
        result = {
            "id": job.id,
            "name": job.name,
            "args": job.args,
            "kwargs": job.kwargs,
            # "function": job.func, # pickled function is not serializable
            "function_ref": job.func_ref,
            "executor": job.executor,
            "next_run_time": str(job.next_run_time)
        }
        return create_result(items=[result], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def pause_one_job(scheduler: BackgroundScheduler, job_id: str):
    try:
        assert job_id, Exception('Job ID was either null or empty')
        job = scheduler.get_job(job_id=job_id)
        result = job.pause()
        return create_result(items=[], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def resume_one_job(scheduler: BackgroundScheduler, job_id: str):
    try:
        assert job_id, Exception('Job ID was either null or empty')
        job = scheduler.get_job(job_id=job_id)
        result = job.resume()
        return create_result(items=[], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def remove_one_job(scheduler: BackgroundScheduler, job_id: str):
    try:
        assert job_id, Exception('Job ID was either null or empty')
        job = scheduler.get_job(job_id=job_id)
        result = job.remove()
        return create_result(items=[], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def update_one_job(scheduler: BackgroundScheduler, job_id: str, payload):
    try:
        result = {}
        return create_result(items=[], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


def add_job(scheduler: BackgroundScheduler, function, function_params=None, **kwargs):
    """
    :param function_params:
    :param scheduler:
    :return:
    :param function: function tp be executed
    """
    stuff = kwargs
    if function_params is None:
        function_params = {}
    triggers = ['cron', 'interval', 'date']
    try:
        # max_instances = 1, coalesce = True, misfire_grace_time = 2 ** 30,
        scheduler.add_job(func=function, **stuff)
        return create_result(items=[], result_=func_name() + '_SUCCESS', status_code=200)
    except Exception as e:
        l.exception(e.__str__())
        return create_result(items=[], result_=func_name() + '_FAILURE', more=e.__str__(), status_code=500)


"""
    Date:
    run_date (datetime|str) – the date/time to run the job at
    timezone (datetime.tzinfo|str) – time zone for run_date if it doesn’t have one already
    
    Cron:
    year (int|str) – 4-digit year
    month (int|str) – month (1-12)    
    day (int|str) – day of month (1-31)    
    week (int|str) – ISO week (1-53)    
    day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)    
    hour (int|str) – hour (0-23)    
    minute (int|str) – minute (0-59)    
    second (int|str) – second (0-59)    
    start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)    
    end_date (datetime|str) – latest possible date/time to trigger on (inclusive)    
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)    
    jitter (int|None) – delay the job execution by jitter seconds at most
    
    Interval:
    weeks (int) – number of weeks to wait
    days (int) – number of days to wait    
    hours (int) – number of hours to wait    
    minutes (int) – number of minutes to wait    
    seconds (int) – number of seconds to wait    
    start_date (datetime|str) – starting point for the interval calculation    
    end_date (datetime|str) – latest possible date/time to trigger on    
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations    
    jitter (int|None) – delay the job execution by jitter seconds at most
"""
