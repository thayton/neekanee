import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Altius Education',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.altiused.com',
    'jobs_page_url': 'http://www.altiused.com/jobs/available-positions',

    'empcnt': [11,50]
}

class AltiusEdJobScraper(JobScraper):
    def __init__(self):
        super(AltiusEdJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': re.compile(r'view-job-listing')}
        d = s.find('div', attrs=x)
        x = {'class': 'field-content'}

        for h3 in d.findAll('h3', attrs=x):
            job = Job(company=self.company)
            job.title = h3.text
            job.url = urlparse.urljoin(self.br.geturl(), h3.a['href'])
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
            x = {'class': re.compile(r'node-jobs')}
            d = s.find('div', attrs=x)
            t = d.find(text=re.compile(r'^Location:'))

            if t:
                l = t.parent.nextSibling
                l = self.parse_location(l)
                if l:
                    job.location = l

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return AltiusEdJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
