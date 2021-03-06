import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Gidsy',
    'hq': 'Berlin, Germany',

    'home_page_url': 'https://gidsy.com',
    'jobs_page_url': 'http://www.getyourguide.com/jobs.php',

    'empcnt': [1,10]
}

class GidsyJobScraper(JobScraper):
    def __init__(self):
        super(GidsyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='jobs-navigation')
        x = {'class': 'jobs-navigation-block'}
        r = re.compile(r'jobs\.php\?id=\d+$')

        for v in d.findAll('div', attrs=x):
            l = self.parse_location(v.h6.text)
            if not l:
                continue

            for a in v.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                job.desc = get_all_text(d)
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='static-pages-content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return GidsyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
