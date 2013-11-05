import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_get, url_query_add

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tektronix Communications',
    'hq': 'Plano, TX',

    'home_page_url': 'http://www.tektronixcommunications.com',
    'jobs_page_url': 'http://tekcomms.jobs/ajax/joblisting/?num_items=50&offset=0',

    'empcnt': [1001,5000]
}

class TektronixJobScraper(JobScraper):
    def __init__(self):
        super(TektronixJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        d = url_query_get(url, ['num_items', 'offset'])
        num_items = int(d['num_items'])
        offset = int(d['offset'])

        self.br.addheaders = [('X-Requested-With', 'XMLHttpRequest')]
        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'direct_joblisting '}
            y = {'class': 'direct_joblocation'}

            if len(s.findAll('li', attrs=x)) == 0:
                break # Done

            for li in s.findAll('li', attrs=x):
                d = li.find('div', attrs=y)
                l = self.parse_location(d.text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = li.a.text
                job.url = urlparse.urljoin(self.br.geturl(), li.a['href'])
                job.location = l
                jobs.append(job)

            offset += num_items
            u = url_query_add(self.br.geturl(), {'offset': '%d' % offset}.items())
            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'itemtype': 'http://schema.org/JobPosting'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TektronixJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
