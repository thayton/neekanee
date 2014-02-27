import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Maryville College',
    'hq': 'Maryville, TN',

    'home_page_url': 'http://www.maryvillecollege.edu',
    'jobs_page_url': 'http://www.maryvillecollege.edu/about/inside/employment/',

    'empcnt': [201,500]
}

class MaryvilleCollegeJobScraper(JobScraper):
    def __init__(self):
        super(MaryvilleCollegeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        links = ['faculty-positions', 'staff']

        self.br.open(url)

        for link in links:
            u = urlparse.urljoin(self.br.geturl(), link)
            self.br.open(u)

            s = soupify(self.br.response().read())
            r = re.compile(r'^/about/inside/employment/\d+/$')

            for a in s.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
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
            x = {'class': 'body'}
            d = s.find('div', attrs=x)
            x = {'data-type': 'page-wrapper'}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MaryvilleCollegeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
