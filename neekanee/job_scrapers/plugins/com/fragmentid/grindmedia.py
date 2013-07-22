import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'GrindMedia',
    'hq': 'San Clemente, CA',

    'home_page_url': 'http://www.grindmedia.com',
    'jobs_page_url': 'http://www.grindmedia.com/careers/',

    'empcnt': [51,200]
}

class GrindMediaJobScraper(JobScraper):
    def __init__(self):
        super(GrindMediaJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        x = {'class': 'job-listing'}
        v = d.find('div', attrs=x)
        x = {'class': 'position'}
        y = {'class': 'location'}
        d.extract()

        self.company.job_set.all().delete()

        for p in v.findAll('span', attrs=x):
            if not p.a:
                continue

            a = p.a
            l = p.parent.find('span', attrs=y)
            l = self.parse_location(l.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l

            z = d.find(attrs={'name' : a['href'][1:]})
            z = z.findParent('div')

            job.desc = get_all_text(z)
            job.save()

def get_scraper():
    return GrindMediaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
