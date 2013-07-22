import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BrightCove',
    'hq': 'Cambridge, MA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.brightcove.com',
    'jobs_page_url': 'http://www.brightcove.com/en/company/careers/open-positions',

    'empcnt': [201,500]
}

class BrightCoveJobScraper(JobScraper):
    def __init__(self):
        super(BrightCoveJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/en/company/careers/open-positions/\w+$')

        for a in s.findAll('a', href=r):
            x = {'class': 'location'}
            v = a.find('div', attrs=x)

            l = self.parse_location(v.text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = self.new_url(self.br.geturl(), a['href'])
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
            x = {'class': 'job-description'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BrightCoveJobScraper()
