import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Hawaii Pacific University',
    'hq': 'Honolulu, HI',

    'ats': 'Ceridian',

    'home_page_url': 'http://www.hpu.edu',
    'jobs_page_url': 'https://www5.recruitingcenter.net/Clients/hpu/PublicJobs/Canviewjobs.cfm',

    'empcnt': [501,1000]
}

class HpuJobScraper(JobScraper):
    def __init__(self):
        super(HpuJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        self.br.open(url)
        self.br.select_form('JobSearch')
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'^controller\.cfm\?jbaction=JobProfile&Job_Id=\d+')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[1].text + ',' + td[2].text
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
            d = s.find('div', id='crs_jobprofile')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return HpuJobScraper()
