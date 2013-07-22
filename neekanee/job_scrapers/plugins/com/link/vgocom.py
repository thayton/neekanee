import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'VGo Communications',
    'hq': 'Nashua, NH',

    'home_page_url': 'http://www.vgocom.com',
    'jobs_page_url': 'http://www.vgocom.com/vgo-careers',

    'empcnt': [11,50]
}

class vGoComJobScraper(JobScraper):
    def __init__(self):
        super(vGoComJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        # Craptastic HTML on this site
        h = self.br.response().read()
        t = h[h.find('<body'):]
        s = soupify(t)
        d = s.find('div', id='node-504')
        x = {'class': 'content'}
        d = d.find('div', attrs=x)
        x = {'target': '_blank'}

        for a in d.findAll('a', attrs=x):
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

        for job in new_jobs:
            self.br.open(job.url)

            h = self.br.response().read()
            t = h[h.find('<body'):]
            s = soupify(t)
            d = s.find('div', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return vGoComJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
