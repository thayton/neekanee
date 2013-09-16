import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Plexxi',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.plexxi.com',
    'jobs_page_url': 'http://www.plexxi.com/about-us/careers-2/',

    'empcnt': [11,50]
}

class PlexxiJobScraper(JobScraper):
    def __init__(self):
        super(PlexxiJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#post-\d+$')

        self.company.job_set.all().delete()

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = s.find('a', id=a['href'][1:])
            x = x.findNext('article')

            while x:
                name = getattr(x, 'name', None)
                if name == 'a' and x.get('href', None) == '#top':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return PlexxiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

