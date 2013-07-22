import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'OMGPOP',
    'hq': 'New York, NY',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.omgpop.com',
    'jobs_page_url': 'http://omgpop.producteev.com/',

    'empcnt': [11,50]
}

class OmgPopJobScraper(JobScraper):
    def __init__(self):
        super(OmgPopJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        v = { 'class': 'job-link' }

        for a in s.findAll('a', attrs=v):
            p = a.div.findAll('span')
            l = self.parse_location(p[2].text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.span.text
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
            r = re.compile('module_job_description_\d+')
            v = { 'id': r, 'class': 'description' }
            d = s.find('div', attrs=v)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return OmgPopJobScraper()
