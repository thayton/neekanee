import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Inmarsat',
    'hq': 'London, England',

    'home_page_url': 'http://www.inmarsat.com',
    'jobs_page_url': 'http://www.inmarsat.com/corporate/careers/job-opportunities/index.htm',

    'empcnt': [501,1000]
}

class InmarsatJobScraper(JobScraper):
    def __init__(self):
        super(InmarsatJobScraper, self).__init__(COMPANY)
        self.br.set_handle_gzip(True)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'primary-list-block'}
        d = s.find('div', attrs=x)
        r = re.compile(r'^/corporate/careers/job-opportunities/[a-z0-9-]+$')

        for a in d.findAll('a', href=r):
            if a.parent.name != 'li' or a.h2 is None:
                continue

            h4 = a.findPrevious('h4')
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
            x = {'class': 'section main-content wysiwyg'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return InmarsatJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
