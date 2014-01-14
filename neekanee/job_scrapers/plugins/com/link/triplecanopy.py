import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Triple Canopy',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.triplecanopy.com',
    'jobs_page_url': 'https://careers.triplecanopy.com/careers/Careers.aspx',

    'empcnt': [11,50]
}

class TripleCanopyJobScraper(JobScraper):
    def __init__(self):
        super(TripleCanopyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        links = ['http://www.triplecanopy.com/careers/corporate-opportunities/',
                 'http://www.triplecanopy.com/careers/operational-opportunities/']

        for url in links:
            self.br.open(url)

            s = soupify(self.br.response().read())
            x = {'class': 'JobLink'}

            for a in s.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[-1].text)
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
            t = s.find('table', id='CRCareers1_tblJobDescr')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return TripleCanopyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
