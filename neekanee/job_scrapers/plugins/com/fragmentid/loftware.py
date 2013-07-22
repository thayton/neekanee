import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Loftware',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.loftware.com',
    'jobs_page_url': 'http://www.loftware.com/company/careers.cfm',

    'empcnt': [51,200]
}

class LoftwareJobScraper(JobScraper):
    def __init__(self):
        super(LoftwareJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h3' and x.text == 'Positions available:'
        h = s.find(f)
        d = h.findParent('div')
        r = re.compile(r'^#\w+')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find('a', attrs={'name' : a['href'][1:]})
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
    return LoftwareJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
