import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'XyberNET',
    'hq': 'San Diego, CA',

    'home_page_url': 'http://www.xyber.net',
    'jobs_page_url': 'http://www.xyber.net/company/employment/company_employment.html',

    'empcnt': [11,50]
}

class XyberNetJobScraper(JobScraper):
    def __init__(self):
        super(XyberNetJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', align='center')
        r = re.compile(r'^company_')

        for a in d.findAll('a', href=r):
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
            d = s.find('blockquote')
            t = d.findParent('td')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return XyberNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
