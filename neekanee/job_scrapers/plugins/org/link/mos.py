import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Museum of Science',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.mos.org',
    'jobs_page_url': 'http://www.mos.org/jobs',

    'empcnt': [201,500]
}

class MosJobScraper(JobScraper):
    def __init__(self):
        super(MosJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'link_hr-opportunity-details'}

        for a in s.findAll('a', attrs=x):
            d = a.findParent('div')

            job = Job(company=self.company)
            job.title = d.h3.text
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
            d = s.find('div', id='hr-opportunity')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MosJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
