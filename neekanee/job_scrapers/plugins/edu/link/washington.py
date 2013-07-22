import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'University of Washington',
    'hq': 'Seattle, WA',

    'home_page_url': 'http://www.washington.edu',
    'jobs_page_url': 'https://uwhires.admin.washington.edu/eng/candidates/default.cfm?szLocationID=88',

    'empcnt': [10001]
}

class BrccJobScraper(JobScraper):
    def __init__(self):
        super(BrccJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('txtjobsearch')
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^default\.cfm\?szCategory=jobprofile')

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
            d = s.find('div', id='uwhires')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BrccJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
