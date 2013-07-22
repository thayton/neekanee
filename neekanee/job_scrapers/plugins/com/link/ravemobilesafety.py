import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Rave Mobile Safety',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.ravemobilesafety.com',
    'jobs_page_url': 'http://www.ravemobilesafety.com/careers/',

    'empcnt': [11,50]
}

class RaveMobileSafetyJobScraper(JobScraper):
    def __init__(self):
        super(RaveMobileSafetyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'title': True, 'href': True}

        for a in s.findAll('a', attrs=x):
            if len(a.text.strip()) == 0:
                continue

            job = Job(company=self.company)
            job.title = a.text
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
            x = {'class': 'content'}
            n = s.find('section', attrs=x)

            job.desc = ''
            while n:
                name = getattr(n, 'name', None)
                if name == 'footer':
                    break
                elif name is None:
                    job.desc += n
                n = n.next
                
            job.save()

def get_scraper():
    return RaveMobileSafetyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
