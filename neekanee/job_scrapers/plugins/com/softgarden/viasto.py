import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Viasto',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.viasto.com',
    'jobs_page_url': 'https://viasto.softgarden-cloud.com/vacancies',

    'empcnt': [11,50]
}

class ViastoJobScraper(JobScraper):
    def __init__(self):
        super(ViastoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'matchValue ProjectGeoLocationCity'}
        r = re.compile(r'/job/\d+/')

        for a in s.findAll('a', href=r):
            d = a.parent.parent
            d = d.find('div', attrs=x)
            l = self.parse_location(d.text)

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

            job.desc = get_all_text(s)
            job.save()

def get_scraper():
    return ViastoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
