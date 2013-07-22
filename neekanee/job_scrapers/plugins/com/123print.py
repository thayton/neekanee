import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': '123 Print',
    'hq': 'Frederick, MD',

    'home_page_url': 'http://www.123print.com',
    'jobs_page_url': 'http://www.123print.com/Opportunity.aspx',

    'empcnt': [51,200]
}

class PrintJobScraper(JobScraper):
    def __init__(self):
        super(PrintJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = {'class': 'HP-questions'}

        self.company.job_set.all().delete()

        for p in s.findAll('span', attrs=a):
            job = Job(company=self.company)
            job.title = p.text

            x = p.findNext('td', attrs={'class': 'HP-answers'})
            t = x.findNext('td')

            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return PrintJobScraper()
        
