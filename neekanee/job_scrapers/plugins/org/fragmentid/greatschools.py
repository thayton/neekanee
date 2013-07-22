import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'GreatSchools',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.greatschools.org',
    'jobs_page_url': 'http://www.greatschools.org/cgi-bin/static/jobs.inc',

    'empcnt': [51,200]
}

class GreatSchoolsJobScraper(JobScraper):
    def __init__(self):
        super(GreatSchoolsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        y = {'name': True, 'id': True}
        a = s.find('a', attrs=y)
        d = a.findParent('div')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', attrs=y):
            h = d.find('a', href='#%s' % a['id'])
            if not h:
                continue

            job = Job(company=self.company)
            job.title = h.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + a['id'])
            job.location = self.company.location
            job.desc = ''

            x = a.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'a' and x.get('id') and x.get('name'):
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return GreatSchoolsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
