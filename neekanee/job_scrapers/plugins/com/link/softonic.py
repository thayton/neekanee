import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Softonic',
    'hq': 'Barcelona, Spain',

    'home_page_url': 'http://www.softonic.com',
    'jobs_page_url': 'http://careers.en.softonic.com/jobs-at-softonic/',

    'empcnt': [201,500]
}

class SoftonicJobScraper(JobScraper):
    def __init__(self):
        super(SoftonicJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='locations')
        r = re.compile(r'/location/[^/]+/$')
        m = re.compile(r'^#job_\d+$')
        
        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            x = {'class': 'department-name'}
            p = a.find('span', attrs=x)
            l = self.parse_location(p.text)

            if not l:
                continue

            u = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(u)
            z = soupify(self.br.response().read())

            for a in z.findAll('a', href=m):
                job = Job(company=self.company)
                job.title = a.parent.h3.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l

                y = {'id': a['href'][1:], 'class': 'job-description'}
                x = z.find('div', attrs=y)

                job.desc = get_all_text(x)
                job.save()

            self.br.back()

def get_scraper():
    return SoftonicJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
