import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mclaren Group',
    'hq': 'Surrey, UK',

    'home_page_url': 'http://www.mclaren.com',
    'jobs_page_url': 'http://www.mclaren-jobs.com/home.html',

    'empcnt': [1001,5000]
}

class MclarenGroupJobScraper(JobScraper):
    def __init__(self):
        super(MclarenGroupJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='dock')
        r1 = re.compile(r'\.php$')
        r2 = re.compile(r'job_detail\.php\?id=\d+$')

        for a in d.findAll('a', href=r1):
            u = urlparse.urljoin(self.br.geturl(), a['href'])

            self.br.open(u)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')

            for a in d.findAll('a', href=r2):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='infoarea')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MclarenGroupJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
