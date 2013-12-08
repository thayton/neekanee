import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tyndall National Institute',
    'hq': 'Cork, Ireland',

    'home_page_url': 'http://www.tyndall.ie',
    'jobs_page_url': 'http://www.tyndall.ie/content/all-vacancies',

    'empcnt': [201,500]
}

class TyndallJobScraper(JobScraper):
    def __init__(self):
        super(TyndallJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        pageno = 2

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^/vacancies/[^/]+$')
        
            for a in s.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TyndallJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
