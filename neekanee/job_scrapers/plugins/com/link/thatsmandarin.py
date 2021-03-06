import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Thats Mandarin',
    'hq': 'Shanghai, China',

    'home_page_url': 'http://www.thatsmandarin.com',
    'jobs_page_url': 'http://www.thatsmandarin.com/career-opportunities',

    'empcnt': [51,200]
}

class ThatsMandarinJobScraper(JobScraper):
    def __init__(self):
        super(ThatsMandarinJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/career-opportunities/\S+$')
        x = re.compile(r'\[([^]]+)')
        
        for a in s.findAll('a', href=r):
            m = re.search(x, a.text)
            l = self.parse_location(m.group(1))

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
            x = {'class': 'career_table'}
            t = s.find('table', attrs=x)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return ThatsMandarinJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
