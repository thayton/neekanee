import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Netronome',
    'hq': 'Santa Clara, CA',

    'home_page_url': 'http://www.netronome.com',
    'jobs_page_url': 'http://www.netronome.com/careers/',

    'empcnt': [51,200]
}

class NetronomeJobScraper(JobScraper):
    def __init__(self):
        super(NetronomeJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        u = s.find('ul', id='menu-careers')
        r = re.compile(r'/careers/north-america/([^/]+)/$')

        self.company.job_set.all().delete()

        for a in u.findAll('a', href=r):
            m = re.search(r, a['href'])
            l = self.parse_location(m.group(1))

            if not l:
                continue

            link = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(link)

            z = soupify(self.br.response().read())            
            x = {'style': 'font-size: large;'}
            y = {'class': 'page-restrict-output'}
            v = z.find('div', attrs=y)
            v.extract()

            for p in v.findAll('span', attrs=x):
                job = Job(company=self.company)
                job.title = p.text
                job.location = l
                job.url = self.br.geturl()
                job.desc = ''

                y = p.next
                while y:
                    name = getattr(y, 'name', None)
                    if name == 'div' and y.get('class', None) == 'clear-line':
                        break
                    elif name is None:
                        job.desc += y
                    y = y.next

                job.save()

            self.br.back()

def get_scraper():
    return NetronomeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
