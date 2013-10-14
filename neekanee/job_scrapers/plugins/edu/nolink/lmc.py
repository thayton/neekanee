import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lees-McRae College',
    'hq': 'Banner Elk, NC',

    'home_page_url': 'http://www.lmc.edu',
    'jobs_page_url': 'http://www.lmc.edu/faculty/human_resources/job_openings.htm',

    'empcnt': [51,200]
}

class LmcJobScraper(JobScraper):
    def __init__(self):
        super(LmcJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        ids = [ 'FacultyPositions', 'StaffPositions' ]

        self.company.job_set.all().delete()

        for id in ids:
            a = s.find('a', id=id)
            t = a.findNext('table')

            for tr in t.findAll('tr'):
                job = Job(company=self.company)
                job.title = tr.h4.text
                job.url = self.br.geturl()
                job.location = self.company.location
                job.desc = get_all_text(tr)
                job.save()

def get_scraper():
    return LmcJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
