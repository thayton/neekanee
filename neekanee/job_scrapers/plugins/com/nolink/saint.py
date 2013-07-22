import re

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SAINT Corporation',
    'hq': 'Bethesda, MD',

    'home_page_url': 'http://www.saintcorporation.com',
    'jobs_page_url': 'http://www.saintcorporation.com/company/saintCareers.html',

    'empcnt': [1,10]
}

class SaintJobScraper(JobScraper):
    def __init__(self):
        super(SaintJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='mainContent')
        d.extract()

        self.company.job_set.all().delete()

        for h in d.findAll('h2'):
            t = h.text.replace('&nbsp;', '')
            if t == '':
                continue

            job = Job(company=self.company)
            job.title = t
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            ns = h.nextSibling
            while ns and getattr(ns, 'name', None) != 'h2':
                if hasattr(ns, 'name') is False: 
                    job.desc += ns
                else:
                    job.desc += get_all_text(ns)

                ns = ns.nextSibling

            job.save()

def get_scraper():
    return SaintJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
