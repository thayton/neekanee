import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Claricode',
    'hq': 'Waltham, MA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.claricode.com',
    'jobs_page_url': 'http://www.claricode.com/jobs/positions.aspx',

    'empcnt': [11,50]
}

class ClaricodeJobScraper(JobScraper):
    def __init__(self):
        super(ClaricodeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('td', attrs={'class': 'mainbody'})
        r = re.compile(r'^/jobs/positions/.*\.aspx')

        for a in t.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        self.company.ats = 'Online form'

        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)
        
        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('td', attrs={'class': 'mainbody'})

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return ClaricodeJobScraper()

