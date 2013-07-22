import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mad*Pow',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.madpow.com',
    'jobs_page_url': 'http://www.madpow.com/Company/Careers.aspx',

    'empcnt': [11,50]
}

class MadPowJobScraper(JobScraper):
    def __init__(self):
        super(MadPowJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'ContentRight'}
        d = s.find('div', attrs=x)
        x = {'class': 'JobPost'}
        d.extract()

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = v.h4.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return MadPowJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
