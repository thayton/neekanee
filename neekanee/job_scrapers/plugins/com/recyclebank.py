import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Recyclebank',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.recyclebank.com',
    'jobs_page_url': 'https://www.recyclebank.com/corporate-info/careers',

    'empcnt': [51,200]
}

class RecycleBankJobScraper(JobScraper):
    def __init__(self):
        super(RecycleBankJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='job-opportunity')
        x = {'class': 'job-opportunity-city'}
        r = re.compile(r'/corporateinfo/index/jobopportunityarticle/id/\d+$')

        for a in s.findAll('a', href=r):
            t = a.text.lower().strip()
            if t == 'read more':
                continue

            l = a.findNext('div', attrs=x)
            l = self.parse_location(l)

            if not l:
                l = self.company.location

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
            x = {'class': 'mainbar'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return RecycleBankJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
