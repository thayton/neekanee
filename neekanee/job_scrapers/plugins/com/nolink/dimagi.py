import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Dimagi',
    'hq': 'Charlestown, MA',

    'contact': 'jobs@dimagi.com',

    'home_page_url': 'http://www.dimagi.com',
    'jobs_page_url': 'http://www.dimagi.com/about/careers/',

    'empcnt': [11,50]
}

class DimagiJobScraper(JobScraper):
    def __init__(self):
        super(DimagiJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'content'})
        d.extract()

        self.company.job_set.all().delete()

        for h2 in d.findAll('h2'):
            job = Job(company=self.company)
            job.title = h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h2.next
            while x:
                name = getattr(x, 'name', None)
                if name == 'h2':
                    break
                elif name is None:
                    job.desc += x
                x = x.next
            
            job.save()

def get_scraper():
    return DimagiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
