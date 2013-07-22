import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'The International Baccalaureate',
    'hq': 'Bethesda, MD',

    'ats': 'Taleo',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.ibo.org',
    'jobs_page_url': 'http://tbe.taleo.net/NA7/ats/careers/jobSearch.jsp?org=IBO&cws=1',

    'empcnt': [51,200]
}

class IboJobScraper(JobScraper):
    def __init__(self):
        super(IboJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.set_all_readonly(False)
        self.br.form['location'] = ['2'] # Maryland
        self.br.submit()

        # Only look for jobs in the Maryland location
        l = self.parse_location('Bethesda, MD')
        r = re.compile(r'/ats/careers/requisition\.jsp')
        s = soupify(self.br.response().read())
        t = s.table

        for a in t.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())

            job.desc = get_all_text(s.table)
            job.save()

def get_scraper():
    return IboJobScraper()
