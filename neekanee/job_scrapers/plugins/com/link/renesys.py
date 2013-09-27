import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Renesys',
    'hq': 'Manchester, NH',

    'home_page_url': 'http://www.renesys.com',
    'jobs_page_url': 'http://www.renesys.com/company/careers/',

    'empcnt': [11,50]
}

class RenesysJobScraper(JobScraper):
    def __init__(self):
        super(RenesysJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'career-wrapper'}
        d = s.find('div', attrs=x)
        f = lambda x: x.name == 'a' and x.parent.name == 'li'

        for a in d.ul.findAll(f):
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
            x = {'class': 'post_header'}
            h = s.find('h1', attrs=x)
            d = h.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return RenesysJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
