import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Akvo',
    'hq': 'Amsterdam, Netherlands',

    'home_page_url': 'https://www.akvo.org',
    'jobs_page_url': 'http://akvo.org/about-us/working-at-akvo/',

    'empcnt': [51,200]
}

class AkvoJobScraper(JobScraper):
    def __init__(self):
        super(AkvoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        
        x = {'class': 'jobList'}
        ul_all = s.findAll('ul', attrs=x)

        for ul in ul_all:
            if ul.h2:
                break

        ul.extract()

        self.company.job_set.all().delete()

        for li in ul.findAll('li'):
            job = Job(company=self.company)
            job.title = li.h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(li)
            job.save()

def get_scraper():
    return AkvoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
