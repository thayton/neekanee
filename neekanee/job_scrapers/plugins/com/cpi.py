import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Computational Physics, Inc.',
    'hq': 'Springfield, VA',

    'benefits': {
        'vacation': [(1,10)],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.cpi.com',
    'jobs_page_url': 'http://www.cpi.com/employment.html',

    'empcnt': [11,50]
}

class CpiJobScraper(JobScraper):
    def __init__(self):
        super(CpiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^employment/job\d+\.html')
        d = { 'class': 'MainListHead' }

        for g in s.findAll('strong', attrs=d):
            p = g.findParent('p')

            for a in p.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(COMPANY['home_page_url'], a['href']) # special case for URL
                job.location = self.company.location

                m = re.findall(r'(\w+, \w+)', g.text)
                if m:
                    l = self.parse_location(m[0])
                    if l:
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
            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return CpiJobScraper()
