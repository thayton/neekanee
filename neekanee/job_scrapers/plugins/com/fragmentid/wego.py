import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wego.com',
    'hq': 'Singapore, Singapore',

    'home_page_url': 'http://www.wego.com',
    'jobs_page_url': 'http://www.wego.com/jobs',

    'empcnt': [51,200]
}

class WegoJobScraper(JobScraper):
    def __init__(self):
        super(WegoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'jobs#j\d+$')
        x = re.compile(r'\(([^)]+)')
        d = s.find('div', id='post-1225')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            m = re.search(x, a.text)
            if m:
                l = self.parse_location(m.group(1))
            else:
                l = re.sub(ur'.*\u2013\s*', '', a.text)
                l = self.parse_location(l)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            job.desc = ''

            i = a['href'].find('#')
            h = d.find('h2', id=a['href'][i+1:])

            if not h:
                continue

            y = h.next
            
            while y:
                name = getattr(y, 'name', None)
                if name == 'h2':
                    break
                elif name is None:
                    job.desc += y
                y = y.next

            job.save()

def get_scraper():
    return WegoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
