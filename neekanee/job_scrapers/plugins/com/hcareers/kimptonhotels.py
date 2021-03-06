import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Kimpton Hotels & Restaurants',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.kimptonhotels.com',
    'jobs_page_url': 'http://www.hcareers.com/seeker/employer-profiles/kimpton-hotel-restaurant-group/jobs?all=true',

    'empcnt': [5001,10000]
}

class KimptonHotelsJobScraper(JobScraper):
    def __init__(self):
        super(KimptonHotelsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'view\?jobAdId=\d+$')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[1].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())

            job.desc = get_all_text(s.html)
            job.save()

def get_scraper():
    return KimptonHotelsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
