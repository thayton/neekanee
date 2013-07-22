import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'MailerMailer',
    'hq': 'Rockville, MD',

    'benefits': {
        'url': 'http://www.mailermailer.com/jobs/benefits/index.rwp',
        'vacation': []
    },

    'home_page_url': 'http://www.mailermailer.com',
    'jobs_page_url': 'http://www.mailermailer.com/jobs/positions/index.rwp',

    'empcnt': [11,50]
}

class MailerMailerJobScraper(JobScraper):
    def __init__(self):
        super(MailerMailerJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'grid_9'})
        d.extract()

        self.company.job_set.all().delete()

        for h2 in d.findAll('h2'):
            job = Job(company=self.company)
            job.title = h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h2.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h2':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return MailerMailerJobScraper()

