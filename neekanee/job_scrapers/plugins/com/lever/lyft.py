import re, urlparse, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lyft',
    'hq': 'San Francisco, CA',

    'home_page_url': 'https://www.lyft.com',
    'jobs_page_url': 'https://jobs.lever.co/lyft/',

    'empcnt': [201,500]
}

class LyftJobScraper(JobScraper):
    def __init__(self):
        super(LyftJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'posting-title'}
        r = re.compile(r'\bsort-by-location\b')
        y = {'class': r}
        
        for a in s.findAll('a', attrs=x):
            sp = a.find('span', attrs=y)
            l = self.parse_location(sp.text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.h5.text
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
            x = {'class': 'content'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return LyftJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
