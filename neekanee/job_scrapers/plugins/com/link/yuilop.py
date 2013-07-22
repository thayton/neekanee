import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Yuilop',
    'hq': 'Barcelona, Spain',

    'home_page_url': 'http://yuilop.com/intl/',
    'jobs_page_url': 'http://yuilop.com/jobs/',

    'empcnt': [11,50]
}

class YuilopJobScraper(JobScraper):
    def __init__(self):
        super(YuilopJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^jobs-')

        for d in s.findAll('div', id=r):
            f = lambda x: x.name == 'a' and x.parent.name == 'div' and x.span
            for a in d.findAll(f):
                job = Job(company=self.company)
                job.title = a.contents[0]
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
            d = s.find('div', id='content')
            t = d.find(text=re.compile(r'Location:'))

            if t:
                l = re.sub(ur'\u2013.*$', '', t.next)
                l = self.parse_location(l)

                if l:
                    job.location = l

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return YuilopJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
