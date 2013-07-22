import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Icon Motosports',
    'hq': 'Portland, OR',

    'home_page_url': 'http://www.rideicon.com',
    'jobs_page_url': 'http://www.rideicon.com/careers/',

    'empcnt': [11,50]
}

class IconJobScraper(JobScraper):
    def __init__(self):
        super(IconJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='categoryGrid')
        x = {'class': 'categoryTitle'}
        d.extract()

        self.company.job_set.all().delete()

        for h in d.findAll('header', attrs=x):
            n = h.findParent('section')
            n = n.next

            job = Job(company=self.company)
            job.title = h.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            while n:
                name = getattr(n, 'name', None)
                if name == 'section':
                    break
                elif name is None:
                    job.desc += n
                n = n.next

            job.save()

def get_scraper():
    return IconJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
