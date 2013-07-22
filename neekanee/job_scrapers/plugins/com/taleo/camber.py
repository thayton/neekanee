import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Camber Corporation',
    'hq': 'Huntsville, AL',

    'ats': 'Taleo',
    'benefits': {'vacation': [(0,10),(3,15),(4,20)]},

    'home_page_url': 'http://www.camber.com',
    'jobs_page_url': 'https://tbe.taleo.net/NA11/ats/careers/jobSearch.jsp?org=CAMBER&cws=1',

    'empcnt': [1001,5000]
}

class CamberJobScraper(JobScraper):
    def __init__(self):
        super(CamberJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'requisition\.jsp\?')

        for l in self.br.links(url_regex=r):
            a = s.find('a', href=l.url)
            x = a.findNext('td').b.string
            x = self.parse_location(x)

            if not x:
                continue

            job = Job(company=self.company)
            job.title = l.text
            job.location = x
            job.url = urlparse.urljoin(self.br.geturl(), l.url)
            job.url = urlutil.url_params_del(job.url)
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find(text='Description').findNext('td')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return CamberJobScraper()
