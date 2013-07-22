import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Electrical Geodesics Incorporated',
    'hq': 'Eugene, OR',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.egi.com',
    'jobs_page_url': 'http://www.egi.com/company/company-employment',

    'empcnt': [51,200]
}

class EgiJobScraper(JobScraper):
    def __init__(self):
        super(EgiJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = attrs={'class': 'contentpaneopen'}
        t = s.find('table', attrs=x)
        r = re.compile(r'/company/company\-employment#\w+')
        t.extract()

        self.company.job_set.all().delete()

        for a in t.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            i = a['href'].find('#') + 1
            x = t.find(attrs={'name' : a['href'][i:]})

            if x is None:
                continue

            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return EgiJobScraper()
