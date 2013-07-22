import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Akvo',
    'hq': 'Amsterdam, Netherlands',

    'home_page_url': 'https://www.akvo.org',
    'jobs_page_url': 'http://www.akvo.org/web/jobs',

    'empcnt': [51,200]
}

class AkvoJobScraper(JobScraper):
    def __init__(self):
        super(AkvoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        
        x = {'class': 'space20'}
        d = s.find('div', attrs=x)
        d.extract()

        r = re.compile(r'^#')

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find(attrs={'name' : a['href'][1:]})
            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'a' and x.get('name', None):
                    break
                elif name is None:
                    job.desc += x
                x = x.next
            
            job.save()

def get_scraper():
    return AkvoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
