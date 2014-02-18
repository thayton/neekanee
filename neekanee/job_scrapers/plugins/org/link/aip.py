import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'American Institute of Physics',
    'hq': 'College Park, MD',

    'home_page_url': 'http://www.aip.org',
    'jobs_page_url': 'http://www.aip.org/aip/employment/',

    'empcnt': [201,500]
}

class AipJobScraper(JobScraper):
    def __init__(self):
        super(AipJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': re.compile(r'view-aip-jobs')}
        d = s.find('div', attrs=x)
        r = re.compile(r'^/aip/jobs/[^/]+$')
        f = lambda x: x.name == 'a' and re.search(r, x.get('href', '')) and x.text == 'More'

        for a in d.findAll(f):
            a = a.findPrevious('a', href=r)
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
            a = s.find('a', id='main-content')
            d = a.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return AipJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
