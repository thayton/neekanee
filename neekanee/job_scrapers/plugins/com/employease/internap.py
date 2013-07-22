import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Internap',
    'hq': 'Atlanta, GA',

    'ats': 'Employease',

    'home_page_url': 'http://www.internap.com',
    'jobs_page_url': 'http://www.internap.com/about-us-internap/careers/job-openings/',

    'empcnt': [201,500]
}

class InternapJobScraper(JobScraper):
    def __init__(self):
        super(InternapJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'/recruit/\?id=\d+')

        for a in d.findAll('a', href=r):
            p = a.parent
            m = re.search(u'\u2013(.*)\u2013', p.contents[-1])
            if not m:
                continue

            l = self.parse_location(m.group(1))
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
            f = s.find('form')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return InternapJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

