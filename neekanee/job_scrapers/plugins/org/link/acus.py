import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Atlantic Council of the United States',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.acus.org',
    'jobs_page_url': 'http://b6.caspio.com/dp.asp?AppKey=58BE2000c3f2d8h4d3c9f4b9g9e0',

    'empcnt': [51,200]
}

class AcusJobScraper(JobScraper):
    def __init__(self):
        super(AcusJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'name': 'cbTable'}
        t = s.find('table', attrs=x)
        r = re.compile(r'^dp\.asp\?\S+RecordID=\d+')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = url_query_filter(job.url, ['appSession', 'RecordID', 'PageID'])
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
            f = s.find('form', id='caspioform')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return AcusJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
