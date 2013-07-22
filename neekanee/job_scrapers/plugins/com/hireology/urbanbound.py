import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'UrbanBound',
    'hq': 'Chicago, IL',

    'home_page_url': 'http://www.urbanbound.com',
    'jobs_page_url': 'http://urbanbound.hireology.com/careers',

    'empcnt': [1,10]
}

class UrbanBoundJobScraper(JobScraper):
    def __init__(self):
        super(UrbanBoundJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='job_content')
        r = re.compile(r'^\d+$')
        x = {'name': r}
        y = {'class': 'headingOrange'}
        f = re.compile(r'^details_\d+$')

        self.company.job_set.all().delete()

        for a in d.findAll('a', attrs=x):
            v = a.findNext('div', attrs=y)
            z = a.findNext('div', id=f)

            t = a.findNext('table')
            l = t.findAll('table')[1]
            l = self.parse_location(l.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = v.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + a['name'])
            job.location = l
            job.desc = get_all_text(z)
            job.save()

def get_scraper():
    return UrbanBoundJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
