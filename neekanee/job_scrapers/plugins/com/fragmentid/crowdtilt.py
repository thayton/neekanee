import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Crowdtilt',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.crowdtilt.com',
    'jobs_page_url': 'https://www.crowdtilt.com/learn/jobs',

    'empcnt': [11,50]
}

class CrowdTiltJobScraper(JobScraper):
    def __init__(self):
        super(CrowdTiltJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-body'}
        d = s.find('div', attrs=x)
        r = re.compile(r'^#job\d+$')

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            i = a['href'].find('#')
            y = {'class': 'job-body', 'id': a['href'][i+1:]}
            v = s.find('div', attrs=y)

            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return CrowdTiltJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
