import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Committee for Economic Development',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.ced.org',
    'jobs_page_url': 'http://www.ced.org/about/employment-internships',

    'empcnt': [201,500]
}

class CedJobScraper(JobScraper):
    def __init__(self):
        super(CedJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/about/employment-internships/')
        x = {'class': 'contentpagetitle', 'href': r}

        for a in s.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
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
            t = s.find('td', attrs={'class': 'mainbody'})

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return CedJobScraper()
