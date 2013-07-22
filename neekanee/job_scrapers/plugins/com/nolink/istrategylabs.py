import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'iStrategyLabs',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.istrategylabs.com',
    'jobs_page_url': 'http://www.istrategylabs.com/about/careers/',

    'empcnt': [11,50]
}

class iStrategyLabsJobScraper(JobScraper):
    def __init__(self):
        super(iStrategyLabsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        n = s.find('section', id='careers')
        x = {'id': True}

        self.company.job_set.all().delete()

        for d in n.findAll('div', attrs=x, recursive=False):
            f = lambda x: x.name == 'dt' and x.text == 'Location'
            t = s.find(f)

            if not t:
                continue

            l = t.findNext('dd')
            l = self.parse_location(l.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = d.h2.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + d['id'])
            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return iStrategyLabsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
