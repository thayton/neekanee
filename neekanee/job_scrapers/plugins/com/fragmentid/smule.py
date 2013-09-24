import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Smule',
    'hq': 'Palo Alto, CA',

    'home_page_url': 'http://www.smule.com',
    'jobs_page_url': 'http://www.smule.com/jobs',

    'empcnt': [11,50]
}

class SmuleJobScraper(JobScraper):
    def __init__(self):
        super(SmuleJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        x = {'class': 'open-positions-panel'}
        d = s.find('div', attrs=x)

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            x = {'name': a['href'][1:]}
            y = s.find('a', attrs=x)
            v = y.findParent('div')

            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return SmuleJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
