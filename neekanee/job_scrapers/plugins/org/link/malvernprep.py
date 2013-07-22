import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Malvern Preparatory School',
    'hq': 'Malvern, PA',

    'home_page_url': 'http://www.malvernprep.org',
    'jobs_page_url': 'http://www.malvernprep.org/careers',

    'empcnt': [51,200]
}

class MalvernPrepJobScraper(JobScraper):
    def __init__(self):
        super(MalvernPrepJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^item\d+$')
        z = re.compile(r'/RelId/\d+/ISvars/default/[^\.]+\.htm$')
        x = {'id': r, 'name': r, 'class': 'title', 'href': z}

        for a in s.findAll('a', attrs=x):
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

        r = re.compile(r'^item\d+$')
        z = re.compile(r'/RelId/\d+/ISvars/default/[^\.]+\.htm$')
        x = {'id': r, 'name': r, 'class': 'title', 'href': z}

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            a = s.find('a', attrs=x)
            t = a.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return MalvernPrepJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
