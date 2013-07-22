import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'AcademicWorks',
    'hq': 'Austin, TX',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.academicworks.com',
    'jobs_page_url': 'http://www.academicworks.com/careers',

    'empcnt': [1,10]
}

class AcademicWorksJobScraper(JobScraper):
    def __init__(self):
        super(AcademicWorksJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        t = d.find(text='Open Positions')
        d = t.findParent('div')
        a = {'class': 'toggle'}

        self.company.job_set.all().delete()

        for h6 in d.findAll('h6', attrs=a):
            x = {'class': 'toggle_div'}
            v = h6.findNext('div', attrs=x)

            job = Job(company=self.company)
            job.title = h6.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return AcademicWorksJobScraper()
