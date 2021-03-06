import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vartopia',
    'hq': 'Washington, DC',

    'ats': 'Taleo',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.vartopia.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA2/ats/careers/jobSearch.jsp?org=VARTOPIA&cws=1&rid=12',

    'empcnt': [11,50]
}

class VartopiaJobScraper(JobScraper):
    def __init__(self):
        super(VartopiaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        s = soupify(self.br.response().read())
        d = s.find('div', id='taleoContent')
        r = re.compile(r'requisition\.jsp')

        for a in d.findAll('a', href=r):
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
            d = s.find('div', id='taleoContent')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return VartopiaJobScraper()
