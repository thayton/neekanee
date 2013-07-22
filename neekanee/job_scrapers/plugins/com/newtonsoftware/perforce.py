import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Perforce',
    'hq': 'Alameda, CA',

    'ats': 'newton',

    'home_page_url': 'http://www.perforce.com',
    'jobs_page_url': 'http://newton.newtonsoftware.com/career/CareerHome.action?clientId=4028f88b2c2b3e87012c2d53b3890fa1',

    'empcnt': [51,200]
}

class PerforceJobScraper(JobScraper):
    def __init__(self):
        super(PerforceJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='gnewtonCareerBody')
        r = re.compile(r'/career/JobIntroduction\.action\?clientId=')
        x = re.compile(r'\((.*)\)')

        for a in d.findAll('a', href=r):
            m = re.search(x, a.text)
            if not m:
                continue

            l = self.parse_location(m.group(1))

            if l is None:
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
            t = s.find('table', id='gnewtonJobDescription')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return PerforceJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
