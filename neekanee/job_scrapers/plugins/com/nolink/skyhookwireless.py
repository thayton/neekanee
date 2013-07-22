import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Skyhook Wireless',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.skyhookwireless.com',
    'jobs_page_url': 'http://www.skyhookwireless.com/whoweare/careers.php',

    'empcnt': [11,50]
}

class SkyhookWirelessJobScraper(JobScraper):
    def __init__(self):
        super(SkyhookWirelessJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        d.extract()

        self.company.job_set.all().delete()

        for h3 in d.findAll('h3'):
            job = Job(company=self.company)
            job.title = h3.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h3.next
            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return SkyhookWirelessJobScraper()
