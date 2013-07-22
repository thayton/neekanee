import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Clark Builders',
    'hq': 'Edmonton, Canada',

    'home_page_url': 'http://www.clarkbuilders.com',
    'jobs_page_url': 'http://www.clarkbuilders.com/job-listings',

    'empcnt': [501,1000]
}

class ClarkBuildersJobScraper(JobScraper):
    def __init__(self):
        super(ClarkBuildersJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/job-details/\d+$')
        
        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-2].text)
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
            d = s.find('div', id='content')
            x = {'class': 'article'}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ClarkBuildersJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
