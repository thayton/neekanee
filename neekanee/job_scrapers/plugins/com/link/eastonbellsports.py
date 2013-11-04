import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Easton-Bell Sports',
    'hq': 'Van Nuys, CA',

    'home_page_url': 'http://www.eastonbellsports.com',
    'jobs_page_url': 'https://www.eastonbellsports.com/careers/search/',

    'empcnt': [1001,5000]
}

class EastonBellSportsJobScraper(JobScraper):
    def __init__(self):
        super(EastonBellSportsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-filter-results'}
        d = s.find('div', attrs=x)
        r = re.compile(r'/careers/details/[^#]+#')

        for a in s.findAll('a', href=r):
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
            x = {'class': 'job-desc-header'}
            y = {'class': 'jobs-detail'}
            d = s.find('div', attrs=x)
            d = d.findParent('div')
            
            t = d.find('div', attrs=y)
            t = t.find(text=re.compile(r'^Location:'))
            l = self.parse_location(t.parent.parent.contents[-1])

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return EastonBellSportsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
