import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Iron Mountain',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.ironmountain.com',
    'jobs_page_url': 'http://ironmountain.jobs/jobs/',

    'empcnt': [10001]
}

class IronMountainJobScraper(JobScraper):
    def __init__(self):
        super(IronMountainJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        s = soupify(self.br.response().read())
        d = s.find('div', id='direct_listingDiv')
        x = {'class': 'direct_joblisting '}
        y = {'class': 'direct_joblocation'}

        for li in d.findAll('li', attrs=x):
            l = li.find('div', attrs=y)
            l = self.parse_location(l.text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = li.a.text
            job.url = urlparse.urljoin(self.br.geturl(), li.a['href'])
            job.location = l
            jobs.append(job)
            break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='direct_innerContainer')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return IronMountainJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
