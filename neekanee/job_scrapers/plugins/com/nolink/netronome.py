import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Netronome',
    'hq': 'Santa Clara, CA',

    'contact': 'careers@netronome.com',

    'home_page_url': 'http://www.netronome.com',
    'jobs_page_url': 'http://www.netronome.com/pages/careers-north-america',

    'empcnt': [51,200]
}

class NetronomeJobScraper(JobScraper):
    def __init__(self):
        super(NetronomeJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = s.find('a', title='North America')
        u = a.findNext('ul')
        r = re.compile(r'^/pages/([\w-]+)-jobs$')

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            u = urlparse.urljoin(self.br.geturl(), a['href'])
            m = re.search(r, a['href'])
            l = m.group(1)

            self.br.open(u)

            x = soupify(self.br.response().read())
            m = x.find('div', attrs={'class': 'page-content'})
            m.extract()

            l = self.parse_location(l)
            
            if not l:
                continue

            for h3 in m.findAll('h3'):
                job = Job(company=self.company)
                job.title = h3.text
                job.location = l
                job.url = self.br.geturl()
                job.desc = ''

                y = h3.next
                while y:
                    name = getattr(y, 'name', None)
                    if name == 'h3':
                        break
                    elif name is None:
                        job.desc += y
                    y = y.next

                job.save()

def get_scraper():
    return NetronomeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
