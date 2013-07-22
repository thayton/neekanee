import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'JPI',
    'hq': 'Blacksburg, VA',

    'benefits': {
        'vacation': [(1,15)],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.jpidev.com',
    'jobs_page_url': 'http://www.jpidev.com/about-us/careers/',

    'empcnt': [11,50]
}

class JpiDevJobScraper(JobScraper):
    def __init__(self):
        super(JpiDevJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        u = s.find('ul', attrs={'class': 'listing'})

        self.company.job_set.all().delete()

        for l in u.findAll('li', recursive=False):
            x = l.h3.span.text
            x = re.sub(r'.*in ', '', x)
            n = self.parse_location(x)

            if not n:
                continue

            job = Job(company=self.company)
            job.title = l.h3.contents[0]
            job.url = self.br.geturl()
            job.location = n
            job.desc = get_all_text(l)
            job.save()

def get_scraper():
    return JpiDevJobScraper()
