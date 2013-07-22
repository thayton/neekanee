import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Institute for Advanced Study',
    'hq': 'Princeton, NJ',

    'home_page_url': 'http://www.ias.edu',
    'jobs_page_url': 'http://www.ias.edu/campus/hr/jobpostings',

    'empcnt': [201,500]
}

class IasJobScraper(JobScraper):
    def __init__(self):
        super(IasJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'^#\S+')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find('a', attrs={'name' : a['href'][1:]})
            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'a' and x.has_key('name'):
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return IasJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
