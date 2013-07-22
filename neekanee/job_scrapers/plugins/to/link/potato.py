import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Potato',
    'hq': 'London, UK',

    'home_page_url': 'http://p.ota.to',
    'jobs_page_url': 'http://p.ota.to/jobs/',

    'empcnt': [51,200]
}

class ProofJobScraper(JobScraper):
    def __init__(self):
        super(ProofJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h2' and x.text == 'By Role'
        h = s.find(f)
        d = h.findParent('div')
        r = re.compile(r'^/jobs/[^/]+/$')

        for a in d.findAll('a', href=r):
            l = a.parent.span
            l = self.parse_location(l.text)

            if not l:
                continue

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
            d = s.find('div', id='jobdetail')
            x = {'class': 'synopsis'}
            p = d.find('p', attrs=x)
            d = p.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ProofJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
