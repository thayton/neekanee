import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Soundrop',
    'hq': 'Oslow, Norway',

    'home_page_url': 'http://soundrop.fm',
    'jobs_page_url': 'http://soundrop.fm/jobs',

    'empcnt': [11,50]
}

class SoundropJobScraper(JobScraper):
    def __init__(self):
        super(SoundropJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#\S+$')
        f = lambda x: x.name == 'a' and x.has_key('href') and re.search(r, x['href']) and x.parent.name == 'li'

        self.company.job_set.all().delete()

        for a in s.findAll(f):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            h = s.find('h2', id=a['href'][1:])
            v = h.findParent('article')

            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return SoundropJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
