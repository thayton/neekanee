import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Internet Systems Consortium',
    'hq': 'Redwood City, CA',

    'home_page_url': 'https://www.isc.org/',
    'jobs_page_url': 'https://www.isc.org/wordpress/about/jobs/',

    'empcnt': [51,200]
}

class IscJobScraper(JobScraper):
    def __init__(self):
        super(IscJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h3' and x.text == 'Open Positions'
        h = s.find(f)
        u = h.findNext('ul')
        r = re.compile(r'/jobs/[^/]+/$')

        for a in u.findAll('a', href=r):
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
            d = s.find('div', id='main')
            x = {'class': re.compile(r'template-page\s+content')}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return IscJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
