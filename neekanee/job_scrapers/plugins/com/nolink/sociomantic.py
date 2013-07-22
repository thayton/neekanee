import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Sociomantic',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.sociomantic.com',
    'jobs_page_url': 'http://careers.sociomantic.com',

    'empcnt': [11,50]
}

class SociomanticJobScraper(JobScraper):
    def __init__(self):
        super(SociomanticJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        jobs = []

        self.br.open(self.company.jobs_page_url)

        position_no = 1

        s = soupify(self.br.response().read())
        d = s.find('div', id='positions')

        self.company.job_set.all().delete()

        while True:
            h2 = d.find('h2', id='position-%d-header' % position_no)
            if not h2:
                break

            x = d.find('div', id='position-%d' % position_no)
            l = self.parse_location(h2.a.span.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = h2.a.contents[0]
            job.url = self.br.geturl()
            job.location = l
            job.desc = get_all_text(x)
            job.save()

            position_no += 1

        return jobs


def get_scraper():
    return SociomanticJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
