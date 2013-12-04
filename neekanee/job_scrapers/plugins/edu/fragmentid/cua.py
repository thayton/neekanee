import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Catholic University of America',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.cua.edu',
    'jobs_page_url': 'http://humanresources.cua.edu/positions/current.cfm',

    'empcnt': [51,200]
}

class CuaJobScraper(JobScraper):
    def __init__(self):
        super(CuaJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        d = s.find('div', id='col1num2')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.parent.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            y = {'name': a['href'][1:]}
            x = d.find('a', attrs=y)
            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'a' and x.has_key('name'):
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return CuaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
