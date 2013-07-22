import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Buena Vista University',
    'hq': 'Storm Lake, IA',

    'benefits': {
        'url': 'http://www.bvu.edu/only_at_bvu/business_services/human_resources/employee_benefits.dot',
        'vacation': [(0,26),(11,27),(13,28),(15,29),(17,30),(19,31)]
    },

    'home_page_url': 'http://www.bvu.edu',
    'jobs_page_url': 'http://www.bvu.edu/bv/human-resources/job-openings.dot',

    'empcnt': [201,500]
}

class BvuJobScraper(JobScraper):
    def __init__(self):
        super(BvuJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'main-content'})
        r = re.compile(r'^listing\-misc\.dot\?inode=\S+$')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
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

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'main-content'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BvuJobScraper()
