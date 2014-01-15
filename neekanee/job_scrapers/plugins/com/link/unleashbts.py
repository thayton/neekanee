import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BTS',
    'hq': 'Columbia, MD',

    'home_page_url': 'http://www.unleashbts.com',
    'jobs_page_url': 'http://www.unleashbts.com/careers',

    'empcnt': [11,50]
}

class UnleashBtsJobScraper(JobScraper):
    def __init__(self):
        super(UnleashBtsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'row')
        x = {'class': r, 'title': True, 'location': True}

        for id in ['full_time', 'internships']:
            d = s.find('div', id=id)
            for v in d.findAll('div', attrs=x):
                l = self.parse_location(v['location'])
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = v.h2.text
                job.url = self.br.geturl()
                job.location = l
                job.desc = get_all_text(v)
                job.save()

def get_scraper():
    return UnleashBtsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
