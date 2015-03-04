import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wistia',
    'hq': 'Somerville, MA',

    'home_page_url': 'http://www.wistia.com',
    'jobs_page_url': 'https://boards.greenhouse.io/wistia',

    'empcnt': [1,10]
}

class WistiaJobScraper(JobScraper):
    def __init__(self):
        super(WistiaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'location'}
        y = {'class': 'opening'}
        r = re.compile(r'^/wistia/jobs/\d+$')
        
        for a in s.findAll('a', href=r):
            d = a.findParent('div', attrs=y)
            p = d.find('span', attrs=x)
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
            d = s.find('div', id='main')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WistiaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
