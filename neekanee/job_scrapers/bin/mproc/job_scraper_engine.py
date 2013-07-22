#!/usr/bin/env python

import urlparse

from job_scraper import JobScraper
from task_manager import TaskManager

class JobScraperEngine(TaskManager):
    def __init__(self, job_scrapers=[]):
        self.job_scrapers = job_scrapers
        self.domains_being_scraped = []

        super(JobScraperEngine, self).__init__(tasks=job_scrapers)

    def get_next_task(self, tasks):
        for job_scraper in tasks:
            if job_scraper.domain not in self.domains_being_scraped:
                self.job_scrapers.remove(job_scraper)
                return job_scraper

        return None

    def task_launched(self, task):
        if task.domain not in self.domains_being_scraped:
            self.domains_being_scraped.append(task.domain)

    def task_completed(self, task):
        self.domains_being_scraped.remove(task.domain)

if __name__ == '__main__':
    import random
    random.seed()

    job_scrapers = []

    job_scrapers.append(JobScraper('www.tenablesecurity.com', 'adp.com'))
    job_scrapers.append(JobScraper('www.blurb.com',           'adp.com'))
    job_scrapers.append(JobScraper('www.edgewave.com',        'adp.com'))

    job_scrapers.append(JobScraper('www.akimeka.com',         'taleo.com'))
    job_scrapers.append(JobScraper('www.camber.com',          'taleo.com'))
    job_scrapers.append(JobScraper('www.qualys.com',          'taleo.com'))

    job_scrapers.append(JobScraper('www.debix.com',           'debix.com'))
    job_scrapers.append(JobScraper('www.ember.com',           'ember.com'))
    job_scrapers.append(JobScraper('www.extole.com',          'extole.com'))

    job_scrapers.append(JobScraper('www.gwu.com',             'peopleadmin.com'))
    job_scrapers.append(JobScraper('www.gmu.com',             'peopleadmin.com'))
    job_scrapers.append(JobScraper('www.jsu.com',             'peopleadmin.com'))

    engine = JobScraperEngine(job_scrapers)
    engine.run()

