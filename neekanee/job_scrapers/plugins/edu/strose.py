import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'The College of Saint Rose',
    'hq': 'Albany, NY',

    'home_page_url': 'http://www.strose.edu',
    'jobs_page_url': 'http://www.strose.edu/officesandresources/employment_opportunities/employmentopportunities',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

class StroseJobScraper(JobScraper):
    def __init__(self):
        super(StroseJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/jobofferdetails\.jsp\?JOBID=\d+')

        for t in s.findAll(text='Click here'):
            if t.parent['id'] != '0':
                continue

            self.br.open(t.parent['href'])

            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'alt': 'Apply Now'}
            i = s.find('input', attrs=x)

            t0 = i.findParent('table')
            t1 = t0.findParent('table')
            tq = t1.findParent('table')

            l = t0.find(text='Locations:').findNext('td').text
            if l.find(';') != -1:
                l = l.rsplit(';', 1)[1]

            l = self.parse_location(l)
            if not l:
                return False

            job.location = l
            job.desc = get_all_text(t1)
            job.save()

def get_scraper():
    return StroseJobScraper()
