import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Electrical Geodesics Incorporated',
    'hq': 'Eugene, OR',

    'home_page_url': 'http://www.egi.com',
    'jobs_page_url': 'http://www.egi.com/company/company-employment',

    'empcnt': [51,200]
}

class EgiJobScraper(JobScraper):
    def __init__(self):
        super(EgiJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = attrs={'itemprop': 'articleBody'}
        d = s.find('div', attrs=x)
        r = re.compile(r'^#')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            i = a['href'].find('#') + 1
            x = {'name' : a['href'][i:]}
            x = d.find(attrs=x)

            if x is None:
                continue

            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return EgiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
