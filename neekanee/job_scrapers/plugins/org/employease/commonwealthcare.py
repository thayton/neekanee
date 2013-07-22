import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Commonwealth Care Alliance',
    'hq': 'Washington, DC',

    'ats': 'Employease',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.commonwealthcare.org',
    'jobs_page_url': 'http://www.commonwealthcare.org/about-us/careers.html',

    'empcnt': [51,200]
}

class CommonwealthCareJobScraper(JobScraper):
    def __init__(self):
        super(CommonwealthCareJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'/recruit/\?id=\d+$')
        done = []

        for a in d.findAll('a', href=r):
            if a['href'] in done:
                continue

            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-1].text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = td[0].text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l

            jobs.append(job)
            done.append(job.url)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form', id='Container0')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return CommonwealthCareJobScraper()
