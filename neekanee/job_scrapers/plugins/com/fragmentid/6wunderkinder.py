import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': '6wunderkinder',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.6wunderkinder.com',
    'jobs_page_url': 'http://www.6wunderkinder.com/en/jobs',

    'empcnt': [11,50]
}

class SixWunderkinderJobScraper(JobScraper):
    def __init__(self):
        super(SixWunderkinderJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-offer'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = d.h2.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + d['id'])
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SixWunderkinderJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
