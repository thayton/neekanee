import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Scribe Software',
    'hq': 'Manchester, NH',

    'home_page_url': 'http://www.scribesoft.com',
    'jobs_page_url': 'http://www.scribesoft.com/Careers',

    'empcnt': [51,200]
}

class ScribeSoftJobScraper(JobScraper):
    def __init__(self):
        super(ScribeSoftJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'name': True, 'id': True}
        a = s.find('a', attrs=x)
        d = a.findParent('div')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', attrs=x):
            h = a.parent
            job = Job(company=self.company)
            job.title = h.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + a['name'])
            job.location = self.company.location
            job.desc = ''

            x = a

            while x:
                name = getattr(x, 'name', None)
                if name == 'hr':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return ScribeSoftJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
