import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Western Wyoming Community College',
    'hq': 'Rock Springs, WY',

    'contact': 'jobs@wwcc.wy.edu',

    'benefits': {
        'url': 'http://www.wwcc.wy.edu/hum_res/benefits.htm',
        'vacation': [(1,20)],
        'holidays': 14,
        'sick_days': 15,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.wwcc.wy.edu',
    'jobs_page_url': 'http://www.wwcc.wy.edu/hum_res/employment.htm',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class WwccWyJobScraper(JobScraper):
    def __init__(self):
        super(WwccWyJobScraper, self).__init__(COMPANY)
    
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^jobs/.*\.pdf$')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = ' '.join(a.text.split())
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return WwccWyJobScraper()
