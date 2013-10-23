import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Concerro',
    'hq': 'Palo Alto, CA',

    'home_page_url': 'http://www.palantir.com',
    'jobs_page_url': 'http://www.palantir.com/careers/OpenPositionLanding',

    'empcnt': [201,500]
}

class PalantirJobScraper(JobScraper):
    def __init__(self):
        super(PalantirJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^/careers/OpenPosDetail\?id=\S+')
            x = re.compile(r'^/careers/OpenPositionLandingLocation\?lc')

            for a in s.findAll('a', href=r):
                l = a.findNext('a', href=x)
                l = self.parse_location(l.text)

                if l is None:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='wrapper')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return PalantirJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
