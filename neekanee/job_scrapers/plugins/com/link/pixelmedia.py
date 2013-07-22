import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Pixel Media',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.pixelmedia.com',
    'jobs_page_url': 'http://www.pixelmedia.com/careers',

    'empcnt': [11,50]
}

class PixelMediaJobScraper(JobScraper):
    def __init__(self):
        super(PixelMediaJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'careerslist'}
        u = s.find('ul', attrs=x)
        r = re.compile(r'^/careers/\S+')

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
            x = {'class': re.compile(r'careerdetails')}
            n = s.find('section', attrs=x)

            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return PixelMediaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
