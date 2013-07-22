import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

class ResumatorJobScraper(JobScraper):
    """ Crawler for the Resumator Applicant Tracking System """
    def __init__(self, company_dict):
        super(ResumatorJobScraper, self).__init__(company_dict)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='resumator-job-listings')
        x = {'class': 'resumator-job-title-link'}
        y = {'class': 'resumator-job-location'}

        for a in d.findAll('a'):
            l = a.findNext('li', attrs=y)
            l = self.parse_location(l.text)

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
            d = s.find('div', id='wrap')

            job.desc = get_all_text(d)
            job.save()
