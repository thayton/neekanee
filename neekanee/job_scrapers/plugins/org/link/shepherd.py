import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Shepherd Center',
    'hq': 'Atlanta, GA',

    'home_page_url': 'http://www.shepherd.org',
    'jobs_page_url': 'https://secure.shepherd.org/employment.nsf/positionsavailable',

    'empcnt': [1001,5000]
}

class ShepherdJobScraper(JobScraper):
    def __init__(self):
        super(ShepherdJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/employment\.nsf/positionsavailable\!OpenForm\S+Expand=\d+')

        for a in s.findAll('a', href=r):
            u = urlparse.urljoin(self.br.geturl(), a['href'])
            u = url_query_filter(u.replace('!', '?'), 'Expand')
            u = u.replace('?', '!OpenForm&')

            self.br.open(u)

            z = soupify(self.br.response().read())
            v = re.compile(r'employment\.nsf/\d+/[A-Z0-9]+\?OpenDocument$')            

            for a in z.findAll('a', href=v):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                job = Job(company=self.company)
                job.title = td[1].text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('fieldset')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return ShepherdJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
