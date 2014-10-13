import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Internap',
    'hq': 'Atlanta, GA',

    'ats': 'Employease',

    'home_page_url': 'http://www.internap.com',
    'jobs_page_url': 'http://www.internap.com/about/careers/current-openings/',

    'empcnt': [201,500]
}

class InternapJobScraper(JobScraper):
    def __init__(self):
        super(InternapJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'section__general-content'}
        d = s.find('div', attrs=x)
        r = re.compile(r'/jobs/apply/posting\.html\?\S+jobId=\d+')

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

            s = self.br.response().read()
            r = re.compile(r'"(/jobs/apply/common/jobLanding\.faces[^"]+)"')
            m = re.search(r, s)
            u = urlparse.urljoin(self.br.geturl(), m.group(1))

            self.br.open(u)

            s = soupify(self.br.response().read())
            b = s.html.body

            job.desc = get_all_text(b)
            job.save()

def get_scraper():
    return InternapJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

