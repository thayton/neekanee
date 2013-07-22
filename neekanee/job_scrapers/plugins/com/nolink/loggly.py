import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Loggly',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.loggly.com',
    'jobs_page_url': 'http://www.loggly.com/company/careers/',

    'empcnt': [11,50]
}

class LogglyJobScraper(JobScraper):
    def __init__(self):
        super(LogglyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'main focus'}
        d = s.find('div', attrs=x)
        d.extract()

        self.company.job_set.all().delete()

        for h3 in d.findAll('h3'):
            title = h3.text.replace('&nbsp;', '')
            if len(title.strip()) == 0:
                continue

            job = Job(company=self.company)
            job.title = title
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h3.next
            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += x
                x = x.next
            
            job.save()

def get_scraper():
    return LogglyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
