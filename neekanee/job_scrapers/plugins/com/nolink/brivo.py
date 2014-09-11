import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Brivo',
    'hq': 'Bethesda, MD',

    'home_page_url': 'http://www.brivo.com',
    'jobs_page_url': 'http://www.brivo.com/about/careers',

    'empcnt': [51,200],
}

class BrivoJobScraper(JobScraper):
    def __init__(self):
        super(BrivoJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        jobs = []

        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        h = s.find('h3', id='open-positions')
        d = h.findNext('div', id='accordion')
        x = {'class': 'panel-title'}
        
        self.company.job_set.all().delete()

        for h4 in d.findAll('h4', attrs=x):
            a = h4.a
            b = h4.findNext('div', id=a['href'][1:])

            job = Job(company=self.company)
            job.title = h4.contents[0]
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = get_all_text(b)
            job.save()

def get_scraper():
    return BrivoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
