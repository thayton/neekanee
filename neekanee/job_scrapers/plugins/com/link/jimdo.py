import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Jimdo',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.jimdo.com',
    'jobs_page_url': 'http://www.jimdo.com/jobs/',

    'empcnt': [51,200]
}

class JimdoJobScraper(JobScraper):
    def __init__(self):
        super(JimdoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/jobs/[^/]+/$')
        
        for id in ['cc-m-4645448314', 'cc-m-4665656714']:
            d = s.find('div', id=id)
            l = self.parse_location(d.h2.text)
            
            if not l:
                continue

            d = d.parent

            for a in d.findAll('a', href=r):
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
            d = s.find('div', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return JimdoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
