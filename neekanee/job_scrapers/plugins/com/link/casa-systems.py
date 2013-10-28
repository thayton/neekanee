import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Casa Systems',
    'hq': 'Andover, MA',

    'home_page_url': 'http://www.casa-systems.com',
    'jobs_page_url': 'http://www.casa-systems.com/company/careers',

    'empcnt': [51,200]
}

class CasaSystemsJobScraper(JobScraper):
    def __init__(self):
        super(CasaSystemsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/company/\S+$')
        t = s.find(text=re.compile(r'OPEN Positions:', re.I))
        x = {'class': 'smallGreyLnk'}
        p = t.findNext('span', attrs=x)
        p.extract()

        for a in p.findAll('a', href=r):
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
            try:
                self.br.open(job.url)
            except:
                continue

            s = soupify(self.br.response().read())
            t = s.find('strong')

            if not t:
                t = s.find('b')
                if not t:
                    continue

            d = t.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CasaSystemsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
