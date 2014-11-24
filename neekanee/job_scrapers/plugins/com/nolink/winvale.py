import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Winvale',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.winvale.com',
    'jobs_page_url': 'http://www.winvale.com/company/careers/',

    'empcnt': [11,50]
}

class WinValeJobScraper(JobScraper):
    def __init__(self):
        super(WinValeJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'tabs-nav'}
        u = s.find('ul', attrs=x)

        x = {'class': 'tabs-container'}
        d = s.find('div', attrs=x)

        r = re.compile(r'^#tab-[\d-]+$')

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            v = d.find('div', id=a['href'][1:])
            
            job = Job(company=self.company)
            job.title = a.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v) 
            job.save()

def get_scraper():
    return WinValeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
