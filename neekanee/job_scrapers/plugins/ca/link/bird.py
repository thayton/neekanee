import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bird Construction',
    'hq': 'Mississauga, Canada',

    'home_page_url': 'http://www.bird.ca',
    'jobs_page_url': 'http://www.bird.ca/Careers/Skilled-Professionals/career-opportunities1/category-CurrentPositions.html',

    'empcnt': [1001,5000]
}

class BirdJobScraper(JobScraper):
    def __init__(self):
        super(BirdJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^Careers/Skilled-Professionals/career-opportunities1/')
        y = re.compile(r'Location: ', re.I)

        for a in s.findAll('a', href=r):
            if not a.b:
                continue

            l = re.sub(y, '', a.contents[-2])
            l = self.parse_location(l)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.b.text
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
            d = s.find('div', id='content')
            x = {'class': 'apply_wrapper'}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BirdJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
