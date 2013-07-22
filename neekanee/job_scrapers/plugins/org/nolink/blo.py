import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Boston Lyric Opera',
    'hq': 'Boston, MA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.blo.org',
    'jobs_page_url': 'http://www.blo.org/about/employment/',

    'empcnt': [11,50]
}

class BloJobScraper(JobScraper):
    def __init__(self):
        super(BloJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        d.extract()

        hr = d.find('hr')

        self.company.job_set.all().delete()

        while hr:
            job = Job(company=self.company)
            job.title = hr.findNext('strong').text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = hr.next
            while x:
                name = getattr(x, 'name', None)
                if name == 'hr':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            hr = hr.findNext('hr')
            job.save()

def get_scraper():
    return BloJobScraper()
