import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'National Consumer Law Center',
    'hq': 'Boston, MA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.nclc.org',
    'jobs_page_url': 'http://www.nclc.org/employment.html',

    'empcnt': [11,50]
}

class NclcJobScraper(JobScraper):
    def __init__(self):
        super(NclcJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='article_wrap')
        d.extract()

        for a in d.findAll('a'):
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

            if job.url.endswith('.pdf'):
                data = pdftohtml(self.br.response().read())
                s = soupify(data)
                job.desc = get_all_text(s.html.body)
            else:
                s = soupify(self.br.response().read())
                d = s.find('div', id='article_wrap')
                job.desc = get_all_text(d)

            job.save()

def get_scraper():
    return NclcJobScraper()

