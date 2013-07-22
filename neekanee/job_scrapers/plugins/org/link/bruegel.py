import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bruegel',
    'hq': 'Brussels, Belgium',

    'home_page_url': 'http://www.bruegel.org',
    'jobs_page_url': 'http://www.bruegel.org/careers/',

    'empcnt': [11,50]
}

class BruegelJobScraper(JobScraper):
    def __init__(self):
        super(BruegelJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/careers/job-detail/job/\S+/$')

        for a in s.findAll('a', href=r):
            if a.parent.name != 'h3':
                continue

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
            x = {'class': 'wide-form'}
            f = s.find('form', attrs=x)

            for v in f.findAll('fieldset'):
              v.extract()

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return BruegelJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
