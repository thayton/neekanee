import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Gidsy',
    'hq': 'Berlin, Germany',

    'home_page_url': 'https://gidsy.com',
    'jobs_page_url': 'https://gidsy.com/jobs/',

    'empcnt': [1,10]
}

class GidsyJobScraper(JobScraper):
    def __init__(self):
        super(GidsyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        u = s.find('ul', id='available-jobs-list')

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            x = {'id': a['href'][1:], 'class': 'job-listing'}
            d = s.find('div', attrs=x)
            
            if not d:
                continue

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return GidsyJobScraper()
