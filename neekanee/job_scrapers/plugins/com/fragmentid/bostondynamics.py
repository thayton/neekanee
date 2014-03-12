import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Boston Dynamics',
    'hq': 'Waltham, MA',

    'home_page_url': 'http://www.bostondynamics.com',
    'jobs_page_url': 'http://www.bostondynamics.com/bd_jobs.html',

    'empcnt': [51,200]
}

class BostonDynamicsJobScraper(JobScraper):
    def __init__(self):
        super(BostonDynamicsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'^#')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.ul.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find('a', attrs={'name' : a['id']})
            x = x.next.findNext(text=re.compile(r'[^\n]'))

            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return BostonDynamicsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
