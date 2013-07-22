import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_params_del

from neekanee_solr.models import *

COMPANY = {
    'name': 'International Food Policy Research Institute (IFPRI)',
    'hq': 'Washington, DC',

    'ats': 'taleo',

    'home_page_url': 'http://www.ifpri.org',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH13/ats/careers/searchResults.jsp?org=IFPRI&cws=37',

    'empcnt': [201,500]
}

class IfpriJobScraper(JobScraper):
    def __init__(self):
        super(IfpriJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'requisition\.jsp')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[2].text)
            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = url_params_del(job.url)
            job.location = l
            jobs.append(job)
            break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='page')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return IfpriJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
