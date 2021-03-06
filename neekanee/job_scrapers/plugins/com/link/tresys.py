import re, urlparse, urllib2

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tresys',
    'hq': 'Columbia, MD',

    'home_page_url': 'http://www.tresys.com',
    'jobs_page_url': 'http://www.tresys.com/careers.php',

    'empcnt': [51,200]
}

class TresysJobScraper(JobScraper):
    def __init__(self):
        super(TresysJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^\./careers/[0-9]+')
        x = re.compile(r'[^-]+-([^-]+)')

        for a in s.findAll('a', href=r):
            m = re.search(x, a.text)
            l = self.parse_location(m.group(1))
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.location = l
            job.url = urlparse.urljoin(self.br.geturl(), urllib2.quote(a['href']))
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.html.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return TresysJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
