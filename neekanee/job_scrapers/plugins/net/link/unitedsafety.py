import re, urlparse, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'United Safety',
    'hq': 'Airdrie, Canada',

    'home_page_url': 'http://www.unitedsafety.net',
    'jobs_page_url': 'http://recruiter.unitedsafety.net/CareerConnector/Job/Search',

    'empcnt': [501,1000]
}

class UnitedSafetyJobScraper(JobScraper):
    def __init__(self):
        super(UnitedSafetyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        json_jobs = json.loads(s.prettify())

        for j in json_jobs:
            l = self.parse_location(j['Location'])
            if not l:
                continue

            job = Job(company=self.company)
            job.title = j['Title']
            job.url = urlparse.urljoin(self.br.geturl(), '/CareerConnector/Job/Details/%s' % j['Job'])
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
            d = s.find('div', id='container')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return UnitedSafetyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
