import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_get

from neekanee_solr.models import *

COMPANY = {
    'name': 'Blount Memorial Hospital',
    'hq': 'Maryville, TN',

    'home_page_url': 'http://www.blountmemorial.org',
    'jobs_page_url': 'https://isc142.bmnet.com/bmhpositioncontrol.nsf/WebMainByTitle?OpenForm',

    'empcnt': [201,500]
}

class BlountMemorialJobScraper(JobScraper):
    def __init__(self):
        super(BlountMemorialJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            x = {'name': '_WebMainByTitle'}
            f = s.find('form', attrs=x)
            r = re.compile(r'bmhpositioncontrol\.nsf\S+\?OpenDocument$')

            n = 0

            for a in f.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)
                n += 1

            if n == 0:
                break

            try:
                self.br.follow_link(self.br.find_link(text='Next'))
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return BlountMemorialJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
