import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BTS',
    'hq': 'Columbia, MD',

    'home_page_url': 'http://www.unleashbts.com',
    'jobs_page_url': 'http://www.unleashbts.com/category/careers/',

    'empcnt': [11,50]
}

class UnleashBtsJobScraper(JobScraper):
    def __init__(self):
        super(UnleashBtsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        pageno = 2

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'post-title'}
        
            for h2 in s.findAll('h2', attrs=x):
                job = Job(company=self.company)
                job.title = h2.a.text
                job.url = urlparse.urljoin(self.br.geturl(), h2.a['href'])
                job.location = self.company.location
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'article'}
            a = s.find('article', attrs=x)
            t = a.find(text=re.compile(r'^Location:'))

            if t:
                l = t.split('Location:')[1]
                l = self.parse_location(l)

                if not l:
                    continue
                else:
                    job.location = l

            job.desc = get_all_text(a)
            job.save()

def get_scraper():
    return UnleashBtsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
