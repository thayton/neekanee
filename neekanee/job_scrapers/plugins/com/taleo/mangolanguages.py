import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mango Languages',
    'hq': 'Farmington Hills, MI',

    'ats': 'Taleo',

    'home_page_url': 'http://www.mangolanguages.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA7/ats/careers/jobSearch.jsp?org=MANGOLANGUAGES&cws=1',

    'empcnt': [51,200]
}

class MangoLanguagesJobScraper(JobScraper):
    def __init__(self):
        super(MangoLanguagesJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'requisition\.jsp[?;]')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = urlutil.url_params_del(job.url)
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return MangoLanguagesJobScraper()
