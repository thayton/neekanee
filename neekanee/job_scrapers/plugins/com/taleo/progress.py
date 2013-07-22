import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Progress Software',
    'hq': 'Boston, MA',

    'ats': 'taleo',
    'benefits': {
        'url': 'http://web.progress.com/en/Careers/na-benefits.html',
        'vacation': []
    },

    'home_page_url': 'http://www.progress.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA5/ats/careers/jobSearch.jsp?org=PROGRESS&cws=1',

    'empcnt': [1001,5000]
}

class ProgressJobScraper(JobScraper):
    def __init__(self):
        super(ProgressJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'requisition\.jsp')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')
        
            l = self.parse_location(td[-1].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = urlutil.url_params_del(job.url)
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

            job.desc = get_all_text(s.table)
            job.save()

def get_scraper():
    return ProgressJobScraper()
