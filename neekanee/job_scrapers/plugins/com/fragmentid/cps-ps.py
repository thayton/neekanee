import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'CPS Professional Services',
    'hq': 'Fairfax, VA',

    'benefits': {
        'url': 'http://www.cps-ps.com/careers/employee-benefits/',
        'vacation': []
    },

    'home_page_url': 'http://www.cps-ps.com',
    'jobs_page_url': 'http://www.cps-ps.com/careers/employment-opportunities/',

    'empcnt': [11,50]
}

class CpsJobScraper(JobScraper):
    def __init__(self):
        super(CpsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        d = {'class': 'ur', 'href': r}

        self.company.job_set.all().delete()

        for a in s.findAll('a', attrs=d):
            job = Job(company=self.company)
            job.title = a.text
            job.location = self.company.location

            x = s.find(attrs={'name' : a['href'][1:]})
            d = x.findNextSibling('div')
            x = {'class': 'uy', 'href': v}
            y = d.find('a', attrs=z)

            if y is not None:
                job.url = urlparse.urljoin(self.br.geturlurl, y['href'])

                self.br.open(job.url)

                c = soupify(self.br.response().read())
                t = c.find(text=job.title)
                d = t.findNext('div')
            else:
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                d = x.findNext('div').findNext('div')

            job.desc = get_all_text(d)
            job.save()
        
def get_scraper():
    return CpsJobScraper()
