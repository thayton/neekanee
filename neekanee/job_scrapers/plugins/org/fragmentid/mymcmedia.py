import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'MyMCMedia',
    'hq': 'Rockville, MD',

    'home_page_url': 'http://www.mymcmedia.org',
    'jobs_page_url': 'http://www.mymcmedia.org/about/jobs/',

    'empcnt': [51,200]
}

class ArchiveJobScraper(JobScraper):
    def __init__(self):
        super(ArchiveJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='plate')
        r = re.compile(r'^#')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            y = {'name': a['href'][1:]}
            v = d.find('a', attrs=y)
            x = {'class': 'job'}
            v = a.findNext('div', attrs=x)
            
            while v:
                name = getattr(v, 'name', None)
                if name == 'a':
                    break
                elif name is None:
                    job.desc += v
                v = v.next

            job.save()

def get_scraper():
    return ArchiveJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
