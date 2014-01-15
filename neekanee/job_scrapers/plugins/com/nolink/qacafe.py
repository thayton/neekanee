import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'QA Cafe',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.qacafe.com',
    'jobs_page_url': 'http://www.qacafe.com/company/careers/',

    'empcnt': [11,50]
}

class QaCafeJobScraper(JobScraper):
    def __init__(self):
        super(QaCafeJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = s.find('article')
        a.extract()

        self.company.job_set.all().delete()

        for h3 in a.findAll('h3'):
            job = Job(company=self.company)
            job.title = h3.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h3.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += ' ' + x
                x = x.next

            job.save()

def get_scraper():
    return QaCafeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
