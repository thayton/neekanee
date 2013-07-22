import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Miso',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://gomiso.com',
    'jobs_page_url': 'http://gomiso.com/jobs',

    'empcnt': [1,10]
}

class GoMisoJobScraper(JobScraper):
    def __init__(self):
        super(GoMisoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        x = {'class': 'secondary'}
        u = s.find('div', attrs=x).ul
        d = s.find('div', id='positions')
        d.extract()

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            x = d.find('div', id=a['href'][1:])

            job.desc = get_all_text(x)

            job.save()

def get_scraper():
    return GoMisoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
