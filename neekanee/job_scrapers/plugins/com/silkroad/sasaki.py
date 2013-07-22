import re, mechanize, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Sasaki Associates',
    'hq': 'Watertown, MA',

    'ats': 'silkroad',

    'home_page_url': 'http://www.sasaki.com',
    'jobs_page_url': 'https://sasaki-openhire.silkroad.com/epostings/index.cfm?fuseaction=app.allpositions&company_id=16623&version=1',

    'empcnt': [201,500]
}

class SasakiJobScraper(JobScraper):
    def __init__(self):
        super(SasakiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'submit\.cfm\?fuseaction=app.jobinfo&jobid=\d+')

        for a in s.findAll('a', href=r):
            d = a.findParent('div')
            l = d.contents[-1]
            l = self.parse_location(l)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = url_query_filter(job.url, ['fuseaction', 'jobid', 'company_id'])
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
            f = s.find('form', id='applyJob')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return SasakiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
