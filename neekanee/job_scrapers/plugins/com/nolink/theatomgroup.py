import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'The Atom Group',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.theatomgroup.com',
    'jobs_page_url': 'http://www.theatomgroup.com/jobs.aspx',

    'empcnt': [11,50]
}

class AtomGroupJobScraper(JobScraper):
    def __init__(self):
        super(AtomGroupJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^\s*Opportunities\s*$')
        h = s.find(text=r)
        d = h.findParent('div')
        x = {'class': 'list1'}
        ul = d.find('ul', attrs=x)

        self.company.job_set.all().delete()

        for li in ul.findAll('li'):
            job = Job(company=self.company)
            job.title = li.h3.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(li)
            job.save()

def get_scraper():
    return AtomGroupJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
