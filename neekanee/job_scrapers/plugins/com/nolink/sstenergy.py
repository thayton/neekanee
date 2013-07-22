import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SST Energy',
    'hq': 'Casper, WY',

    'home_page_url': 'http://www.sstenergy.com',
    'jobs_page_url': 'http://www.sstenergy.com/careers.htm',

    'empcnt': [51,200]
}

class SSTEnergyJobScraper(JobScraper):
    def __init__(self):
        super(SSTEnergyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'Location: (.*)$')
        f = lambda x: x.name == 'p' and x.parent.name == 'th' and x['class'] == 'title'
        g = lambda x: x.name == 'p' and re.search(r, x.text)

        self.company.job_set.all().delete()

        for p in s.findAll(f):
            tr = p.findParent('tr')
            l = tr.find(g)
            m = re.search(r, l.text)
            l = self.parse_location(m.group(1))

            if not l:
                continue

            job = Job(company=self.company)
            job.title = p.text
            job.url = self.br.geturl()
            job.location = l
            job.desc = get_all_text(tr)
            job.save()

def get_scraper():
    return SSTEnergyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
