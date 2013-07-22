import re, urlparse

from jobscraper import JobScraper
from location import parse_location
from soupify import soupify, get_all_text

from neekanee_solr.models import *

class JobScoreJobScraper(JobScraper):
    def __init__(self, company_dict, follow_iframe=False):
        company_dict['ats'] = 'JobScore'
        self.follow_iframe = follow_iframe
        super(JobScoreJobScraper, self).__init__(company_dict)

    def scrape_job_links(self, url):
        jobs = []

        if self.follow_iframe:
            self.br.open(url)
            s = soupify(self.br.response().read())
            url = s.iframe['src']

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = { 'class': 'job-listing' }

        for tr in s.findAll('tr', attrs=d):
            td = tr.findAll('td')
            l = self.parse_location(td[1].text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = tr.a.text
            job.url = urlparse.urljoin(self.br.geturl(), tr.a['href'])
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
            x = {'class': 'rounded_590_mid'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()
