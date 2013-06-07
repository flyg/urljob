from models import UrlJob
from models import UrlJobStatus
from datetime import datetime
import hashlib
import random
from data import url_job


### provider
providers = []

# server provider calls it to register itself
def register_url_job_provider(category, sub_category, provider):
    if get_provider(category, sub_category) is None:
        providers.add([category, sub_category, provider])

# find a provider given category and sub_category
def get_provider(category, sub_category):
    for provider in providers:
        if provider[0]==category and provider[1]==sub_category:
            return provider[2]
    return None


### url_job
# server provider calls it to register a url job
def register_url_job(url, category, sub_category, interval_minutes):
    if not UrlJob.objects.filter(url = url).exists():
        UrlJob.objects.create(
            url = url,
            category = category,
            sub_category = sub_category,
            interval_minutes = interval_minutes,
            status = UrlJobStatus.Idle,
            last_delivered_time = datetime.min,
            last_result_has = '')

# get an url job given url
def get_url_job(url):
    return UrlJob.objects.get(url = url)


### api

# client calls it remotely to retrieve a list of urls to process
def get_jobs(count):
    now = datetime.now()
    job_defs = UrlJob.objects.all().sort(key = lambda x: - (now - x.last_delivered_time).total_minutes() / x.interval_minutes * (1 + random.random(-0.1, 0.1)))
    jobs = []
    for i in range(0, job_defs.len()):
        if i < count:
            job = url_job(url = job_defs[i].url, category = job_defs[i].category, sub_category = job_defs[i].sub_category)
            jobs.add(job)
    return jobs

# client calls it remotely to post a url job result
def post_url_job_result(url_job, result):
    job_def = get_url_job(url_job.url)
    job_def.last_delivered_time = datetime.now()
    job_def.last_result_hash = hashlib.sha256(result).hexdigest()
    job_def.status = UrlJobStatus.Idle
    provider = get_provider(url_job.category, url_job.sub_category)
    provider.process_result(url_job, result)
