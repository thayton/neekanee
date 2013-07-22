import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Media Matters for America', 
    'hq': 'Washington, DC',

    'home_page_url': 'http://mediamatters.org',
    'jobs_page_url': 'http://mediamatters.org/jobs',

    'empcnt': [11,50]
}

class MediaMattersJobScraper(JobScraper):
    def __init__(self):
        super(MediaMattersJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'issues job-index'}
        r = re.compile(r'/jobs/\d{4}/\d{2}/\d{2}/\S+/\d+$')
        ul = s.find('ul', attrs=x)

        for a in ul.findAll('a'):
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
            x = {'class': 'bd-main job-openings item'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MediaMattersJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
