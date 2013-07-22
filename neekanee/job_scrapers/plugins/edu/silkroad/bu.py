import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Boston University',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.bu.edu',
    'jobs_page_url': 'http://www.bu.edu/hr/jobs/open-job-opportunities/',

    'empcnt': [5001,10000]
}

class BuJobScraper(JobScraper):
    def __init__(self):
        super(BuJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form(nr=1)
        self.br.submit()
        self.br.follow_link(self.br.find_link(text='All Posted Jobs'))

        s = soupify(self.br.response().read())
        r = re.compile(r'/epostings/submit.cfm\?fuseaction=app\.jobinfo')

        for a in s.findAll('a', href=r):
            l = a.parent.contents[3]
            l = self.parse_location(l)
            
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
            d = s.find('div', id='text')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BuJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
