import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'YouSendIt',
    'hq': 'Campbell, CA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.yousendit.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA8/ats/careers/jobSearch.jsp?org=YOUSENDIT&cws=1',

    'empcnt': [51,200]
}

class YouSendItJobScraper(JobScraper):
    def __init__(self):
        super(YouSendItJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        r = re.compile(r'requisition\.jsp\?')
        s = soupify(self.br.response().read())
    
        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-2].text)
            if l is None:
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
            t = s.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return YouSendItJobScraper()
