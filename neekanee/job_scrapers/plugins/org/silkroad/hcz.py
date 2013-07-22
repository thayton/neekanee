import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Harlem Childrens Zone',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.hcz.org',
    'jobs_page_url': 'https://hcz-openhire.silkroad.com/epostings/index.cfm?fuseaction=app.allpositions',

    'empcnt': [1001,5000]
}

class HczJobScraper(JobScraper):
    def __init__(self):
        super(HczJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'cssAllJobListBody'}
        d = s.find('div', attrs=x)
        r = re.compile(r'^/epostings/submit\.cfm\?fuseaction=app\.jobinfo&jobid=\d+')
        x = {'class': 'cssAllJobListPositionHref', 'href': r}

        for a in d.findAll('a', attrs=x):
            l = a.parent.contents[-1]
            l = self.parse_location(l)
            
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
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
            f = s.find('form', id='applyJob')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return HczJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
