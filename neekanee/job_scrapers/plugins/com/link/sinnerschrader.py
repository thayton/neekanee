import re, urlparse, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SinnerSchrader',
    'hq': 'Hamburg, Germany',

    'home_page_url': 'http://www.sinnerschrader.com',
    'jobs_page_url': 'http://www.sinnerschrader.com/en/api/jobs/get_all_jobs/',

    'empcnt': [201,500]
}

class SinnerSchraderJobScraper(JobScraper):
    def __init__(self):
        super(SinnerSchraderJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = self.br.response()
        j = json.loads(r.read())
        j.pop('status')

        for k,v in j.items():
            l = self.parse_location(v['location'])
            if not l:
                continue

            job = Job(company=self.company)
            job.title = v['title']
            job.url = v['link']
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
            d = s.find('div', id='post_content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SinnerSchraderJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
