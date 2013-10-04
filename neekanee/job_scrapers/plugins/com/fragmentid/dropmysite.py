import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Dropmysite',
    'hq': 'Singapore, Singapore',

    'home_page_url': 'http://www.dropmysite.com',
    'jobs_page_url': 'https://www.dropmysite.com/en/careers',

    'empcnt': [11,50]
}

class DropMySiteJobScraper(JobScraper):
    def __init__(self):
        super(DropMySiteJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#position-\S+$')
        x = {'class': 'container-general-inner'}
        d = s.find('div', attrs=x)
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''
            
            y = d.find('a', id=a['href'][1:])
            y = y.next

            while y:
                name = getattr(y, 'name', None)
                if name == 'a' and y.get('id', None):
                    break
                elif name is None:
                    job.desc += y
                y = y.next

            job.save()

def get_scraper():
    return DropMySiteJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
