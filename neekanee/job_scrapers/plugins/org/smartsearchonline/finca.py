import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.urlutil import url_query_get
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'FINCA',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.finca.org',
    'jobs_page_url': 'http://search6.smartsearchonline.com/finca/jobs/adhocjobsearch.asp',

    'empcnt': [5001,10000]
}

class FincaJobScraper(JobScraper):
    def __init__(self):
        super(FincaJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('Referrer',
                               'http://search6.smartsearchonline.com/finca/jobs/process_jobsearch.asp'),]

    def scrape_job_links(self, url):
        jobs = []
        
        def select_form(form):
            return form.attrs.get('action', None) == 'process_jobsearch.asp'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'^jobdetails\.asp\?')
        
        for a in s.findAll('a', href=r):
            d = url_query_get(a['href'], 'job_number')

            job = Job(company=self.company)
            job.title = a.text
            job.url = 'http://www.finca.org/job-posting/?id=' + d['job_number']
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
            b = s.find('body', id='careers')

            job.desc = get_all_text(b)
            job.save()

def get_scraper():
    return FincaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
