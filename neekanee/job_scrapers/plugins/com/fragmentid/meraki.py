import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Meraki',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://meraki.com',
    'jobs_page_url': 'https://meraki.cisco.com/jobs',

    'empcnt': [51,200]
}

class MerakiJobScraper(JobScraper):
    def __init__(self):
        super(MerakiJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        n = s.find('section', id='positions')
        x = {'class': 'job-nav-title'}

        self.company.job_set.all().delete()

        for li in n.findAll('li', attrs=x):
            y = {'data-tab': li.a['href'][1:]}
            d = n.find('div', attrs=y)

            job = Job(company=self.company)
            job.title = li.a.contents[0]
            job.url = self.br.geturl()
            job.desc = get_all_text(d)
            job.location = self.company.location
            job.save()

def get_scraper():
    return MerakiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
