import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Institute for Advanced Study',
    'hq': 'Annapolis, MD',

    'home_page_url': 'http://www.sjca.edu',
    'jobs_page_url': 'http://www.sjc.edu/annapolis/personnel/openings/',

    'empcnt': [51,200]
}

class SjcaJobScraper(JobScraper):
    def __init__(self):
        super(SjcaJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#\S+')
        f = lambda x: x.name == 'a' and re.search(r, x.get('href', '')) and x.parent.name == 'li'
        a = s.find(f)
        d = a.findParent('div')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll(f):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            y = {'name': a['href'][1:]}
            x = d.find('a', attrs=y)

            if x is None:
                continue

            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return SjcaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
