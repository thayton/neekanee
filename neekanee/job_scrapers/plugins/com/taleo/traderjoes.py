import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Trader Joes',
    'hq': 'Needham, MA',

    'home_page_url': 'http://www.traderjoes.com',
    'jobs_page_url': 'http://sj.tbe.taleo.net/CH14/ats/careers/jobSearch.jsp?org=TRADERJOES&cws=1',

    'empcnt': [10001]
}

class TraderJoesJobScraper(JobScraper):
    def __init__(self):
        super(TraderJoesJobScraper, self).__init__(COMPANY)

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

            l = td[1].text
            if l.find('Trader Joe'):
                l = l.rsplit(',')
                if len(l) <= 2:
                    continue

                l = l[-2] + ', ' + l[-1].split()[0]

            l = self.parse_location(l)
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
            t = s.find('div', id='taleoContent')
            t = t.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return TraderJoesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
