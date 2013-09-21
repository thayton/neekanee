import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Birmingham-Southern College',
    'hq': 'Birmingham, AL',

    'benefits': {
        'url': 'http://www.bsc.edu/administration/humanresources/benefits.cfm',
        'vacation': [(0,12),(4,18),(16,24)],
        'holidays': 9,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.bsc.edu',
    'jobs_page_url': 'http://www.bsc.edu/administration/humanresources/job_descriptions.cfm',

    'empcnt': [201,500]
}

class BscJobScraper(JobScraper):
    def __init__(self):
        super(BscJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'id': True, 'name': True}

        self.company.job_set.all().delete()

        for a in s.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.parent.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + a['id'])
            job.location = self.company.location
            job.desc = ''

            x = a.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'a' and x.has_key('name'):
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return BscJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
