import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vecima',
    'hq': 'Saskatoon, SK, Canada',

    'home_page_url': 'http://www.vecima.com',
    'jobs_page_url': 'http://www.vecima.com/career-opportunities/',

    'empcnt': [501,1000],
}

class VecimaJobScraper(JobScraper):
    def __init__(self):
        super(VecimaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^post-\d+$')
#        x = {'class': 'vcm-article', 'id': r}

        for a in s.findAll('article', id=r):
            l = a.nextSibling.text
            l = re.sub(r'&#.*', '', l)
            l = self.parse_location(l)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a.a['href'])
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
            r = re.compile(r'^post-\d+$')
            a = s.find('article', id=r)

            job.desc = get_all_text(a)
            job.save()

def get_scraper():
    return VecimaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
