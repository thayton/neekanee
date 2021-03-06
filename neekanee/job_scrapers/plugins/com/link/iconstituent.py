import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'iConstituent',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.iconstituent.com',
    'jobs_page_url': 'http://iconstituent.com/careers/',

    'empcnt': [51,200]
}

class IConstituentJobScraper(JobScraper):
    def __init__(self):
        super(IConstituentJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/careers/[^/]+/$')
        f = lambda x: x.name == 'a' and re.search(r, x['href']) and x.parent.name == 'h3'

        for a in s.findAll(f):
            job = Job(company=self.company)
            job.title = a.text
            job.location = self.company.location
            job.url = urlparse.urljoin(url, a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            r = re.compile(r'^itemid_\d+$')
            d = s.find('div', id=r)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return IConstituentJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
