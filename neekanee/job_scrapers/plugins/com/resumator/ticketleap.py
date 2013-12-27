import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ticket Leap',
    'hq': 'Philadelphia, PA',

    'home_page_url': 'http://www.ticketleap.com',
    'jobs_page_url': 'http://www.ticketleap.com/info/careers',

    'empcnt': [11,50]
}

class TicketLeapJobScraper(JobScraper):
    def __init__(self):
        super(TicketLeapJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'current-openings'}
        n = s.find('section', attrs=x)
        x = {'class': 'opening-title'}

        self.company.job_set.all().delete()

        for h5 in n.findAll('h5', attrs=x):
            li = h5.findParent('li')
            job = Job(company=self.company)
            job.title = h5.findNext(text=True)
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(li)
            job.save()

def get_scraper():
    return TicketLeapJobScraper()
