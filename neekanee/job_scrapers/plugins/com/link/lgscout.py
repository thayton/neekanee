import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lookingglass',
    'hq': 'Arlington, VA',

    'home_page_url': 'http://www.lgscout.com',
    'jobs_page_url': 'http://www.lgscout.com/careers',

    'empcnt': [11,50]
}

class LgscoutJobScraper(JobScraper):
    def __init__(self):
        super(LgscoutJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h3' and x.text == 'Current Openings'
        h = s.find(f)
        u = h.findNext('ul')
        r = re.compile(r'/about-us/careers/[a-zA-Z-]+$')
        
        for a in u.findAll('a', href=r):
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

            s = soupify(self.br.response().read())
            d = s.find('div', id='left-content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return LgscoutJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
