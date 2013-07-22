import re, urlparse, webcli

from jobscraper import JobScraper
from location import parse_location
from soupify import soupify, get_all_text

from neekanee_solr.models import *

class Resumator:
    """ Crawler for the Resumator Applicant Tracking System """
    def __init__(self):
        pass

    def get_jobs(self, c):
        c['ats'] = 'Resumator'
        url = c['jobs_page_url']

        s = soupify(webcli.get(url))
        d = s.find('div', attrs={'class': 'resumator-home-joblist'})

        for a in d.findAll('a'):
            d = a.findParent('div')
            l = d.findNext('div').contents[2]
            l = parse_location(l)

            job = {}
            job['title'] = a.text
            job['link'] = urlparse.urljoin(url, a['href'])
            job['location'] = l
            c['jobs'].append(job)

        for job in c['jobs']:
            s = soupify(webcli.get(job['link']))
            d = s.find('div', id='resumator-job-description')
            job['desc'] = get_all_text(d)

class ResumatorJobScraper(JobScraper):
    """ Crawler for the Resumator Applicant Tracking System """
    def __init__(self, company_dict):
        super(ResumatorJobScraper, self).__init__(company_dict)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'resumator-home-joblist'}
        d = s.find('div', attrs=x)

        for a in d.findAll('a'):
            d = a.findParent('div')
            l = d.findNext('div').contents[2]
            l = self.parse_location(l)

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
            d = s.find('div', id='resumator-job-description')

            job.desc = get_all_text(d)
            job.save()
