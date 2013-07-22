import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Des Moines University',
    'hq': 'Des Moines, IA',

    'benefits': {
        'vacation': [(0,24)],
        'holidays': 9,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.dmu.edu',
    'jobs_page_url': 'http://www.dmu.edu/employment/positions/',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

class DmuJobScraper(JobScraper):
    def __init__(self):
        super(DmuJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        i = s.find('iframe')

        self.br.open(i['src'])
        self.br.select_form('JobSearch')
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'controller\.cfm\?jbaction=JobProfile&Job_Id=\d+')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])

            t = a.parent.findNextSiblings('td', limit=2)
            l = t[0].text + ',' + t[1].text
            l = self.parse_location(l)

            if not l:
                continue

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
            t = s.find('td', attrs={'class': 'regular'})

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return DmuJobScraper()
