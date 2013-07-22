import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Embedded Systems Design',
    'hq': 'Elkridge, MD',

    'contact': 'mark.wecht@embedded-sys.com',
    'benefits': {
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.embedded-sys.com',
    'jobs_page_url': 'http://www.embedded-sys.com/current_jobs.php',

    'empcnt': [11,50]
}

class EmbeddedSysJobScraper(JobScraper):
    def __init__(self):
        super(EmbeddedSysJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile('Applicants for our')

        self.company.job_set.all().delete()

        for t in s.findAll(text=r):
            job = Job(company=self.company)
            job.title = t.nextSibling.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            #
            # Skip "positions must have ..." to get to
            # list of required skills
            #
            curr = t.nextSibling
            prev = curr.previousSibling

            while not (getattr(curr, 'name', None) == 'br' and \
                       getattr(prev, 'name', None) == 'br'):

                prev = curr
                curr = curr.nextSibling

            #
            # Collect list of required skills
            #
            prev = curr
            curr = curr.nextSibling

            while not (getattr(curr, 'name', None) == 'br' and \
                       getattr(prev, 'name', None) == 'br'):

                if hasattr(curr, 'name') is False: 
                    job.desc += curr
                else:
                    job.desc += ''.join(curr.findAll(text=True))

                prev = curr
                curr = curr.nextSibling

            job.save()

def get_scraper():
    return EmbeddedSysJobScraper()
