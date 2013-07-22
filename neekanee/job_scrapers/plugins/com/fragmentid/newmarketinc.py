import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Newmarket International',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://newmarketinc.com',
    'jobs_page_url': 'http://newmarketinc.com/careers/',

    'empcnt': [201,500]
}

class NewmarketIncJobScraper(JobScraper):
    def __init__(self):
        super(NewmarketIncJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r"javascript:showdivbyid\('([^']+)'")
        d = s.find('div', id='mainContainer')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            m = re.search(r, a['href'])
            if not m:
                continue

            x = d.find('div', id=m.group(1))
            i = a.findNextSibling('i')

            if not i:
                continue

            l = self.parse_location(i.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + m.group(1))
            job.location = self.company.location
            job.desc = get_all_text(x)
            job.save()

def get_scraper():
    return NewmarketIncJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
