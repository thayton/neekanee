import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Dorchester House', 
    'hq': 'Dorchester, MA',

    'benefits': {
        'url': 'http://www.dorchesterhouse.org/about/careers/apply-online/',
        'vacation': []
    },

    'home_page_url': 'http://www.dorchesterhouse.org',
    'jobs_page_url': 'http://www.dorchesterhouse.org/about/careers/current-openings/',

    'empcnt': [51,200]
}

class DorchesterHouseJobScraper(JobScraper):
    def __init__(self):
        super(DorchesterHouseJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'\?p=\d+$')
        d = s.find('div', id='content')
        d.extract()

        for a in d.findAll('a', href=r):
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
            p = s.find('p', attrs={'class': 'headline'})
            t = p.findParent('td')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return DorchesterHouseJobScraper()
        
