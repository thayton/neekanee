import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tilera',
    'hq': 'San Jose, CA',

    'home_page_url': 'http://www.tilera.com',
    'jobs_page_url': 'http://tilera.com/company/?ezchip=634',

    'empcnt': [51,200]
}

class TileraJobScraper(JobScraper):
    def __init__(self):
        super(TileraJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#.+')

        self.company.job_set.all().delete()

        for a in s.findAll('a', href=r):
            b = a
            x = {'name': a['href'][1:]}
            a = s.find('a', attrs=x)

            t = a.findParent('table')
            tr = t.findAll('tr')
            td = tr[1].findAll('td')

            l = self.parse_location(td[-1].text)
            if not l:
                continue
            
            job = Job(company=self.company)
            job.title = b.text
            job.url = urlparse.urljoin(self.br.geturl(), b['href'])
            job.location = l
            job.desc = ''
            
            x = a.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'a' and x.get('name', None):
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return TileraJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
