import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wingspan',
    'hq': 'Blue Bell, PA',

    'home_page_url': 'http://www.wingspan.com',
    'jobs_page_url': 'http://www.wingspan.com/career_open_positions/',

    'empcnt': [11,50]
}

class WingSpanJobScraper(JobScraper):
    def __init__(self):
        super(WingSpanJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        d = s.find('div', id='content')
        d = d.find('div', attrs={'class': 'entry-content'})
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find(id=a['href'][1:])
            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'hr' and x.get('id', None):
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return WingSpanJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
