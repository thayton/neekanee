import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Fenway Community Health',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.fenwayhealth.org',
    'jobs_page_url': 'http://www.fenwayhealth.org/site/PageServer?pagename=FCHC_abt_about_employment',

    'empcnt': [51,200]
}

class FenwayHealthJobScraper(JobScraper):
    def __init__(self):
        super(FenwayHealthJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#\d+$')
        d = s.find('div', id='infograybox')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            if a.text == '':
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find('a', attrs={'name' : a['href'][1:]})
            if not x:
                r = re.compile(r'\[Job ID %s\]' % a['href'])
                x = d.find(text=r)
                if not x:
                    continue

            x = x.next

            while x:
                if getattr(x, 'name', None) == 'a' and \
                        x.text == 'back to top':
                    break
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return FenwayHealthJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
