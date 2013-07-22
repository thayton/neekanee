import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

COMPANY = {
    'name': 'Booyah',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.booyah.com',
    'jobs_page_url': 'http://www.booyah.com/jobs/',
    'jobs_page_domain': 'mycompas.com',

    'empcnt': [11,50]
}

class BooyahJobScraper(JobScraper):
    def __init__(self):
        super(BooyahJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='main')
        r = re.compile(r'/jobs/[^/]+/')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.h1.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def get_job_id(self, url):
        u = urlparse.urlparse(url)
        qs = urlparse.parse_qs(u.query)
        return qs['ID'][0]
        
    def scrape_jobs(self):
        self.company.ats = 'compas'
        
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)
            self.br.follow_link(self.br.find_link(name='compframe', tag='iframe'))

            s = soupify(self.br.response().read())
            p = s.find('span', id='lbljobdesc')
            
            job.desc = get_all_text(p)
            job.save()

def get_scraper():
    return BooyahJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
