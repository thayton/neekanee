import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Dropbox',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.dropbox.com',
    'jobs_page_url': 'https://www.dropbox.com/jobs/all',

    'empcnt': [11,50]
}

class DropboxJobScraper(JobScraper):
    def __init__(self):
        super(DropboxJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile('^/jobs/listing/\d+$')
        x = {'class': 'job-title', 'href': r}
        y = {'class': 'job-position-location'}

        for a in s.findAll('a', attrs=x):
            d = a.findParent('div')
            p = d.find('span', attrs=y)
            l = self.parse_location(p.text)

            if not l:
                continue

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
            d = s.find('div', id='page-content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DropboxJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
