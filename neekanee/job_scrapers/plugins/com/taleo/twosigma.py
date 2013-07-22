import re, urlparse, urlutil, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Two Sigma Investments',
    'hq': 'New York, NY',

    'ats': 'Taleo',

    'home_page_url': 'http://www.twosigma.com',
    'jobs_page_url': 'https://ch.tbe.taleo.net/CH02/ats/careers/searchResults.jsp?org=TWOSIGMA&cws=38',

    'empcnt': [201,500]
}

class TwoSigmaJobScraper(JobScraper):
    def __init__(self):
        super(TwoSigmaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        try:
            self.br.select_form('TBE_theForm')
            self.br.submit()
        except mechanize.FormNotFoundError:
            pass

        s = soupify(self.br.response().read())
        r = re.compile(r'requisition\.jsp(;jsessionid=[^?]+)?\?')

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
            h = s.find('h1')
            t = h.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return TwoSigmaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
