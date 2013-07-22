import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'CERN',
    'hq': 'Geneva, Switzerland',

    'home_page_url': 'http://home.web.cern.ch',
    'jobs_page_url': 'http://jobs.web.cern.ch',

    'empcnt': [1001,5000]
}

class CernJobScraper(JobScraper):
    def __init__(self):
        super(CernJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'views-exposed-form-jobs-page-1'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        s = soupify(self.br.response().read())
        x = {'class': re.compile(r'view-jobs')}
        d = s.find('div', attrs=x)
        r = re.compile(r'/job/\d+$')
        
        for a in d.findAll('a', href=r):
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
            n = s.find('section', id='section-content')
            x = {'class': re.compile(r'view-job-details')}
            d = n.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CernJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
