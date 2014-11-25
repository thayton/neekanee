import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Search Optics',
    'hq': 'San Diego, CA',

    'home_page_url': 'http://www.searchoptics.com',
    'jobs_page_url': 'http://www.searchoptics.com/careers',

    'empcnt': [11,50]
}

class SearchOpticsJobScraper(JobScraper):
    def __init__(self):
        super(SearchOpticsJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^careers/\d+$')
        x = { 'class': 'job-title' }
        y = { 'class': 'job-location' }
        z = { 'class': 'job-container' }

        for a in s.findAll('a', href=r):
            d = a.findParent('div', attrs=z)
            t = d.find('h2', attrs=x)
            l = d.find('h3', attrs=y)
            l = self.parse_location(l.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = t.text
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
            x = {'class': 'joblisting'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SearchOpticsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

