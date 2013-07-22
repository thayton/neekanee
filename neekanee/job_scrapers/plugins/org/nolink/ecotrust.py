import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ecotrust',
    'hq': 'Portland, OR',

    'home_page_url': 'http://www.ecotrust.org',
    'jobs_page_url': 'http://ecotrustforests.com/jobs.html',

    'empcnt': [11,50]
}

class EcoTrustJobScraper(JobScraper):
    def __init__(self):
        super(EcoTrustJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#\w+')
        d = s.find('div', id='content')
        f = lambda x: x.text == 'TITLE:' and x.name == 'strong'
        d.extract()

        self.company.job_set.all().delete()

        for t in d.findAll(f):
            p = t.findParent('p')
            job = Job(company=self.company)
            job.title = t.nextSibling.strip()
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = p
            while x:
                if getattr(x, 'name', None) == 'p' and x.text.startswith('###'):
                    break
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return EcoTrustJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
