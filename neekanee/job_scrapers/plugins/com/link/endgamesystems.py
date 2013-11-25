import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Endgame',
    'hq': 'Atlanta, GA',

    'home_page_url': 'http://www.endgame.com',
    'jobs_page_url': 'http://endgame.com/careers.html',

    'empcnt': [51,200]
}

class EndgameJobScraper(JobScraper):
    def __init__(self):
        super(EndgameJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        ul = s.find('ul', id='ind-jobs')
        r = re.compile(r'^/job/[^.]+\.html$')
        
        for a in ul.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.h2.text
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
            x = {'role': 'main'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return EndgameJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()