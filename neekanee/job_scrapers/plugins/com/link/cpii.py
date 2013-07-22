import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Communications & Power Industries',
    'hq': 'Palo Alto, CA',

    'home_page_url': 'http://www.cpii.com',
    'jobs_page_url': 'http://www.cpii.com/opportunities.cfm',

    'empcnt': [1001,5000]
}

class ProofJobScraper(JobScraper):
    def __init__(self):
        super(ProofJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', id='matrix')
        r = re.compile(r'opportunities\.cfm/\d/\d+$')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[0].text)
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
            d = s.find('div', id='content')
            d = d.find('div', id='jobinfo')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ProofJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
