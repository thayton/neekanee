import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Housing Opportunities Commission of Montgomery County',
    'hq': 'Kensington, MD',

    'home_page_url': 'http://www.hocmc.org',
    'jobs_page_url': 'http://www.hocmc.org/Careers/',

    'empcnt': [201,500]
}

class HocmcJobScraper(JobScraper):
    def __init__(self):
        super(HocmcJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='mainContent')
        r = re.compile(r'default\.aspx\?id=\d+')

        for a in d.findAll('a', href=r):
            t =  a.findParent('table')
            tr = t.tr
            td = tr.findAll('td')

            job = Job(company=self.company)
            job.title = td[0].text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            a = {'class': 'moduleTitle'}
            h = s.find('h2', attrs=a)
            t = h.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return HocmcJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
