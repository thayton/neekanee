import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': ' Intelligent Automation',
    'hq': 'Rockville, MD',

    'home_page_url': 'http://www.i-a-i.com',
    'jobs_page_url': 'http://www.i-a-i.com/?careers',

    'empcnt': [51,200]
}

class IAIJobScraper(JobScraper):
    def __init__(self):
        super(IAIJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='articleBody')
        r = re.compile(r'recruit/\?id=\d+$')

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
            f = s.find('form', id='Container0')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return IAIJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
