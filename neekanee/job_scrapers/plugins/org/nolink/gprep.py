import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Georgetown Preparatory School',
    'hq': 'North Bethesda, MD',

    'home_page_url': 'http://www.gprep.org',
    'jobs_page_url': 'http://www.gprep.org/page.cfm?p=434',

    'empcnt': [51,200]
}

class GPrepJobScraper(JobScraper):
    def __init__(self):
        super(GPrepJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        t = s.find('td', id='contentdiv')
        r = re.compile(r'contentElement')
        x = {'class': r}

        self.company.job_set.all().delete()

        for a in t.findAll('a', href='#'):
            d = a.findNext('div', attrs=x)
            job = Job(company=self.company)
            job.title = a.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return GPrepJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
