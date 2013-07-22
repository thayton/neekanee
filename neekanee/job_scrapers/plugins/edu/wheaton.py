import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wheaton College',
    'hq': 'Wheaton, IL',

    'home_page_url': 'http://www.wheaton.edu',
    'jobs_page_url': 'http://www2.wheaton.edu/HR/employment/openings_staff.php',

    'empcnt': [501,1000]
}

class WheatonJobScraper(JobScraper):
    def __init__(self):
        super(WheatonJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('td', id='contentCell')
        r = re.compile(r'^/HR/employment/openings_staff\.php\?id=\d+$')

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
            t = s.find('td', id='contentCell')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return WheatonJobScraper()
