import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Iridium Satellite Communications',
    'hq': 'McLean, VA',

    'ats': 'iApplicants',

    'home_page_url': 'http://www.iridium.com',
    'jobs_page_url': 'http://iridium.iapplicants.com/searchjobs.php',

    'empcnt': [51,200]
}

class IridiumSatelliteJobScraper(JobScraper):
    def __init__(self):
        super(IridiumSatelliteJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^ViewJob')

        for a in s.findAll('a', href=r):
            tr = a.parent.parent
            td = tr.findAll('td')

            l = self.parse_location(td[-1].text)
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
            h = s.h2
            t = h.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return IridiumSatelliteJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
