import re, urlparse, urlutil, urllib, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Netflix',
    'hq': 'Los Gatos, CA',

    'home_page_url': 'http://www.netflix.com',
    'jobs_page_url': 'http://jobs.netflix.com/services/index.php/api/costcenter?function_id=1%20active',

    'empcnt': [1001,5000]
}

class NetflixJobScraper(JobScraper):
    def __init__(self):
        super(NetflixJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        d = json.loads(self.br.response().read())

        for cost_center in d['data']:
            for j in cost_center['jobs']:
                l = self.parse_location(j['Location'])
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = j['Job_Posting_Title']
                job.location = l
                job.url = 'http://jobs.netflix.com/jobs.php?id=' + j['Job_Req_Id']
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='job-detail-url')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NetflixJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
