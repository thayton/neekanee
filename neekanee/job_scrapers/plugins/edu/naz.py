import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Nazareth College',
    'hq': 'Rochester, NY',

    'benefits': {
        'url': 'http://www.naz.edu/human-resources/employee-benefits',
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.naz.edu',
    'jobs_page_url': 'https://jobs.naz.edu',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class NazJobScraper(JobScraper):
    def __init__(self):
        super(NazJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/dept/faculty_position_postings/')
        a = s.find('a', href=r)

        self.br.open(a['href'])

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'showhide'})

        self.company.job_set.all().delete()

        for h in d.findAll('h3'):
            job = Job(company=self.company)
            job.title = h.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(h.findNext('div'))
            job.save()

def get_scraper():
    return NazJobScraper()
