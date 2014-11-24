import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Computer Emergency Response Team (CERT)',
    'hq': 'Pittsburgh, PA',

    'home_page_url': 'http://www.cert.org',
    'jobs_page_url': 'http://www.cert.org/careers/',

    'jobs_page_domain': 'taleo.net',

    'empcnt': [501,1000]
}

class CertJobScraper(JobScraper):
    def __init__(self):
        super(CertJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())

        x = {'class': 'careersTitle'}
        y = {'class': re.compile(r'\bjobEntry\b')}
        z = {'class': 'careersDescription'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            l = d.contents[-1]
            l = self.parse_location(l)

            if not l:
                continue

            p = d.findParent('div', attrs=y)
            v = p.find('div', attrs=z)

            m = {'class': 'careersApply'}
            a = p.find('div', attrs=m)

            job = Job(company=self.company)

            if getattr(d, 'b', None):
                job.title = d.b.text
            elif getattr(d, 'strong', None):
                job.title = d.strong.text
            else:
                continue

            job.url = a.a['href']
            job.location = l
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return CertJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
