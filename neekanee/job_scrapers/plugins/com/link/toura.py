import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Toura',
    'hq': 'New York, NY',

    'contact': 'jobs@toura.com',

    'home_page_url': 'http://toura.com',
    'jobs_page_url': 'http://toura.com/jobs/',

    'empcnt': [11,50]
}

class TouraJobScraper(JobScraper):
    def __init__(self):
        super(TouraJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobs'}
        b = s.find('body', attrs=x)
        x = {'class': 'element widget job-location'}
        r = re.compile(r'^/jobs/\S+')

        for a in b.findAll('a', href=r):
            l = a.findNext('div', attrs=x)

            if not l:
                continue

            l = l.text.lower().split('location:')[1]
            l = self.parse_location(l)

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
            h = s.find('h1', attrs={'class': 'post-title'})
            n = h.findParent('article', attrs={'class': 'detail-article'})

            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return TouraJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
