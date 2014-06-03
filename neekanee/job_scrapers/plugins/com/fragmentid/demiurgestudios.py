import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Demiurge Studios',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.demiurgestudios.com',
    'jobs_page_url': 'http://www.demiurgestudios.com/careers',

    'empcnt': [11,50]
}

class DemiurgeStudiosJobScraper(JobScraper):
    def __init__(self):
        super(DemiurgeStudiosJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='mainContent')
        u = d.find('ul', attrs={'class': 'openings'})
        r = re.compile(r'^#')
        d.extract()

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            y = {'name' : a['href'][1:]}
            x = d.find('a', attrs=y)
            
            if not x:
                continue

            x = x.findNext('h3').next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += x
                x = x.next
                
            job.save()

def get_scraper():
    return DemiurgeStudiosJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
