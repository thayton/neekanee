import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Xtera Communications',
    'hq': 'Allen, TX',

    'home_page_url': 'http://www.xtera.com',
    'jobs_page_url': 'http://www.xtera.com/Company/Careers.aspx',

    'empcnt': [501,1000]
}

class XteraJobScraper(JobScraper):
    def __init__(self):
        super(XteraJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        n = s.find('section', id='content')
        r = re.compile(r'/Company/Careers/[\w-]+\.aspx$')
        x = {'href': r, 'id': True}

        for a in n.findAll('a', attrs=x):
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
            x = {'class': 'content-item details'}
            d = s.find('div', attrs=x)
            l = d.header.h5
            l = self.parse_location(l.text)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return XteraJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
