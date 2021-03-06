import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'National Democratic Institute (NDI)',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.ndi.org',
    'jobs_page_url': 'http://ndi.force.com/careers',

    'empcnt': [1001,5000]
}

class NdiJobScraper(JobScraper):
    def __init__(self):
        super(NdiJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        # XXX TODO handle pagination
        self.br.open(url)

        r = re.compile(r'/careers/ts2__JobDetails\?jobId=\w+')
        s = soupify(self.br.response().read())

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-1].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.location = l
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = urlutil.url_query_filter(job.url, 'jobId')
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='atsJobDetailsBox')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NdiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
