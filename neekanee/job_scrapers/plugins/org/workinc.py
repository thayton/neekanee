import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'WORK Inc',
    'hq': 'Dorchester, MA',

    'benefits': {
        'url': 'http://www.workinc.org/job-posting/benefits/',
        'vacation': []
    },

    'home_page_url': 'http://www.workinc.org',
    'jobs_page_url': 'http://www.workinc.org/job-posting/jobs/',

    'empcnt': [11,50]
}

class WorkIncJobScraper(JobScraper):
    def __init__(self):
        super(WorkIncJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        z = {'class': 'entry-content'}
        d = s.find('div', attrs=z)
        r = re.compile(r'/job-posting/jobs/[\w-]+/$')
        x = {'class': 'job-table'}

        for t in d.findAll('table', attrs=x):
            for a in t.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)
        
        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'job-table'}
            t = s.find('table', attrs=x)
            tr = t.findAll('tr')
            l = self.parse_location(tr[2].td.text)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return WorkIncJobScraper()
