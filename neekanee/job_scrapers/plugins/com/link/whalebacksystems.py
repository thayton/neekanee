import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Whaleback Systems',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.whalebacksystems.com',
    'jobs_page_url': 'http://www.whalebacksystems.com/company/careers',

    'empcnt': [11,50]
}

class WhalebackSystemsJobScraper(JobScraper):
    def __init__(self):
        super(WhalebackSystemsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/company/career/[a-z0-9_]+')
        
        for a in s.findAll('a', href=r):
            if a.parent.name != 'li':
                continue

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
            x = {'class': re.compile(r'page-header')}
            h = s.find('h1', attrs=x)
            d = h.findNextSibling('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WhalebackSystemsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
