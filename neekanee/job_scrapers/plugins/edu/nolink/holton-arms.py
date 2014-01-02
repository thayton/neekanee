import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Holton-Arms School',
    'hq': 'Bethesda, MD',

    'home_page_url': 'http://www.holton-arms.edu',
    'jobs_page_url': 'http://www.holton-arms.edu/page.cfm?p=62',

    'empcnt': [51,200]
}

class HoltonArmsJobScraper(JobScraper):
    def __init__(self):
        super(HoltonArmsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#$')

        self.company.job_set.all().delete()

        for a in s.findAll('a', href=r):
            if len(a.attrs) != 1:
                continue

            x = {'class': re.compile(r'contentElement')}
            d = a.findNext('div', attrs=x)

            job = Job(company=self.company)
            job.title = a.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return HoltonArmsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
