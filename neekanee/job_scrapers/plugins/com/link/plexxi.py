import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Plexxi',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.plexxi.com',
    'jobs_page_url': 'http://www.plexxi.com/about-us/',

    'empcnt': [11,50]
}

class PlexxiJobScraper(JobScraper):
    def __init__(self):
        super(PlexxiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='divJobs')
        r = re.compile(r'/job/[^/]+/$')
        
        for a in d.findAll('a', href=r):
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
            r = re.compile(r'Location:')
            t = s.find(text=r)
            
            if t:
                l = t.split(':')[1]
                l = self.parse_location(l)
                if l:
                    job.location = l

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return PlexxiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

