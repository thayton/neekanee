import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'John Snow, Inc',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.jsi.com',
    'jobs_page_url': 'http://www.jsi.com/JSIInternet/Jobs/index.cfm',

    'empcnt': [1001,5000]
}

class JsiJobScraper(JobScraper):
    def __init__(self):
        super(JsiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='main-content')
        r = re.compile(r'jobdescription\.cfm\?id=\d+')

        for a in d.findAll('a', href=r):
            l = a.text.split('-')[1]
            l = self.parse_location(l)

            if l is None:
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
            d = s.find('div', id='job-description-container')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return JsiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
