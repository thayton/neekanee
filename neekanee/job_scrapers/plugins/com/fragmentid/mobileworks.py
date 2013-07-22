import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'MobileWorks',
    'hq': 'Berkeley, CA',

    'home_page_url': 'https://www.mobileworks.com',
    'jobs_page_url': 'https://www.mobileworks.com/careers/',

    'empcnt': [1,10]
}

class MobileWorksJobScraper(JobScraper):
    def __init__(self):
        super(MobileWorksJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'job_blurb\b')
        x = {'class': r}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = d.h4.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + d.h4['id'])
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MobileWorksJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
