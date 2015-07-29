import re, urlparse

from neekanee.urlutil import url_query_add
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Work Market',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.workmarket.com',
    'jobs_page_url': 'https://boards.greenhouse.io/embed/job_board/?for=workmarket',

    'empcnt': [11,50]
}

class WorkMarketJobScraper(JobScraper):
    def __init__(self):
        super(WorkMarketJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'\?gh_jid=(\d+)$')
        x = {'class': 'location'}

        for a in s.findAll('a', href=r):
            d = a.findParent('div')
            l = d.find('span', attrs=x)
            l = self.parse_location(l.text)

            m = re.search(r, a['href'])

            url = self.company.jobs_page_url.replace('job_board', 'job_app')
            url = url_query_add(url, [ ('token', m.group(1)) ])

            job = Job(company=self.company)
            job.title = a.text
            job.url = url
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
            d = s.find('div', id='app_body')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WorkMarketJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

