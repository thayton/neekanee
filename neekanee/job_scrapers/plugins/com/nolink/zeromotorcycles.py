import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Zero Motorcycles',
    'hq': 'Scotts Valley, CA',

    'home_page_url': 'http://www.zeromotorcycles.com',
    'jobs_page_url': 'http://www.zeromotorcycles.com/company/employment.php',

    'empcnt': [51,200]
}

class ZeroMotorcyclesJobScraper(JobScraper):
    def __init__(self):
        super(ZeroMotorcyclesJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='main-content')
        x = {'class': 'section'}
        r = re.compile(r'^mailto:hr@')
        d.extract()

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            if not v.h2:
                continue

            a = v.find('a', href=r)
            if not a:
                continue

            job = Job(company=self.company)
            job.title = v.h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return ZeroMotorcyclesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
