import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Rocky Mountain Institute',
    'hq': 'Snowmass, CO',

    'home_page_url': 'http://www.rmi.org',
    'jobs_page_url': 'http://www.rmi.org/rmi/Careers',

    'empcnt': [51,200]
}

class RmiJobScraper(JobScraper):
    def __init__(self):
        super(RmiJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h2' and x.text == 'Current Openings'
        h = s.find(f)
        u = h.findNext('ul')
        r = re.compile(r'^#')

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            if len(a.text) == 0:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = s.find('a', attrs={'name': a['href'][1:]})

            while x:
                name = getattr(x, 'name', None)
                if name == 'h2':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return RmiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
