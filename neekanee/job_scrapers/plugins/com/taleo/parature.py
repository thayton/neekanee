import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Parature',
    'hq': 'Vienna, VA',

    'ats': 'taleo',

    'home_page_url': 'http://www.parature.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA7/ats/careers/jobSearch.jsp?org=PARATURE&cws=1',

    'empcnt': [51,200]
}

class ParatureJobScraper(JobScraper):
    def __init__(self):
        super(ParatureJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'careers/requisition\.jsp')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            x = td[-1].text.upper().replace('CORPORATE OFFICE -', '')
            x = self.parse_location(x)

            if not x:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.location = x
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = urlutil.url_params_del(job.url)
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
            t = d.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return ParatureJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
