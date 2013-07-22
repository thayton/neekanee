import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'EDCTP',
    'hq': 'The Hague, The Netherlands',

    'home_page_url': 'http://www.edctp.org',
    'jobs_page_url': 'http://www.edctp.org/Vacancies.143.0.html',

    'empcnt': [11,50]
}

class EdctpJobScraper(JobScraper):
    def __init__(self):
        super(EdctpJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('ul', id='submenu').find(text='Vacancies')
        u = t.findNext('ul')

        for a in u.findAll('a'):
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
            d = s.find('div', id='page_title')
            t = d.findParent('td')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return EdctpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
