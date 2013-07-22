import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Zulily',
    'hq': 'Seattle, WA',

    'home_page_url': 'http://www.zulily.com',
    'jobs_page_url': 'http://www.zulily.com/jobs',

    'empcnt': [501,1000]
}

class ZulilyJobScraper(JobScraper):
    def __init__(self):
        super(ZulilyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/careers/[a-zA-Z0-9]+/$')
        x = {'class': 'position', 'data-url': r}
        y = {'class': 'location'}

        for li in s.findAll('li', attrs=x):
            l = li.find('span', attrs=y)
            l = self.parse_location(l.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = li.span.text
            job.url = urlparse.urljoin(self.br.geturl(), li['data-url'])
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
            x = {'class': 'position-details'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ZulilyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
