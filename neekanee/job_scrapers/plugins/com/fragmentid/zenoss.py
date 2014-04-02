import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Zenoss',
    'hq': 'Annapolis, MD',

    'home_page_url': 'http://www.zenoss.com',
    'jobs_page_url': 'http://zenoss.com/about/jobs',

    'empcnt': [51,200]
}

class ZenossJobScraper(JobScraper):
    def __init__(self):
        super(ZenossJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='career-right-box')
        r = re.compile(r'^#\d+$')

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            y = {'name' : a['href'][1:]}
            x = s.find(attrs=y)

            if not x:
                continue

            z = {'class': 'career-item-list'}
            u = x.findNext('ul', attrs=z)

            job.desc = get_all_text(u)
            job.save()

def get_scraper():
    return ZenossJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
