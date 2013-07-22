import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Dreamworks Animation',
    'hq': 'Glendale, CA',

    'home_page_url': 'http://www.dreamworksanimation.com',
    'jobs_page_url': 'http://www.dreamworksanimation.com/company/careers/jobs',

    'empcnt': [1001,5000]
}

class DprJobScraper(JobScraper):
    def __init__(self):
        super(DprJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobList'}
        d = s.find('div', attrs=x)
        y = {'class': 'jobItem'}

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=y):
            l = self.parse_location(v['location'])
            if not l:
                continue

            job = Job(company=self.company)
            job.title = v['title']
            job.url = urlparse.urljoin(self.br.geturl(), '?jobId=' + v['href'])
            job.location = l
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return DprJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
