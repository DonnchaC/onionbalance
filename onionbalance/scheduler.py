# -*- coding: utf-8 -*-
"""
Simple scheduler for running jobs at regular intervals
"""
import functools
import time

from onionbalance import log

logger = log.get_logger()

jobs = []


class Job(object):
    """
    Object to represent a scheduled job task
    """

    def __init__(self, interval, job_func, *job_args, **job_kwargs):
        self.interval = interval
        self.planned_run_time = time.time()

        # Configure the job function and calling arguments
        self.job_func = functools.partial(job_func, *job_args, **job_kwargs)
        functools.update_wrapper(self.job_func, job_func)

    def __lt__(self, other):
        """
        Jobs are sorted based on their next scheduled run time
        """
        return self.planned_run_time < other.planned_run_time

    @property
    def should_run(self):
        """
        Check if the job should be run now
        """
        return self.planned_run_time <= time.time()

    def run(self, override_run_time=None):
        """
        Run job then reschedule it in the job list
        """
        logger.debug("Running {}".format(self))
        ret = self.job_func()

        # Pretend the job was scheduled now, if we ran it early with run_all()
        if override_run_time:
            self.planned_run_time = time.time()
        self.planned_run_time += self.interval

        return ret

    def __repr__(self):
        """
        Return human readable representation of the Job and arguments
        """
        args = [repr(x) for x in self.job_func.args]
        kwargs = ["{}={}".format(k, repr(v)) for
                  k, v in self.job_func.keywords.items()]
        return "{}({})".format(self.job_func.__name__,
                               ', '.join(args + kwargs))


def add_job(interval, function, *job_args, **job_kwargs):
    """
    Add a job to be executed at regular intervals

    The `interval` value is in seconds, starting from now.
    """
    job = Job(interval, function, *job_args, **job_kwargs)
    jobs.append(job)


def _run_job(job, override_run_time=False):
    """
    Run a job and put it back in the job queue
    """
    return job.run(override_run_time)


def run_all(delay_seconds=0):
    """
    Run all jobs at `delay_seconds` regardless of their schedule
    """
    for job in jobs:
        _run_job(job, override_run_time=True)
        time.sleep(delay_seconds)


def run_forever(check_interval=1):
    """
    Run jobs forever
    """
    while True:
        if not jobs:
            logger.error("No scheduled jobs found, scheduler exiting.")
            return None

        jobs_to_run = (job for job in jobs if job.should_run)
        for job in sorted(jobs_to_run):
            _run_job(job)

        time.sleep(check_interval)
