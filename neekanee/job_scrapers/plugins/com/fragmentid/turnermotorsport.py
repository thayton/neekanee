import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Turner Motorsport',
    'hq': 'Amesbury, MA',

    'home_page_url': 'http://www.turnermotorsport.com',
    'jobs_page_url': 'http://www.turnermotorsport.com/t-employment.aspx',

    'empcnt': [51,200]
}

class TurnerMotorsportJobScraper(JobScraper):
    def __init__(self):
        super(TurnerMotorsportJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        x = {'class': 'colcontent'}

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = v.h4.a.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + v.h4.a['name'])
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return TurnerMotorsportJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
