import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Fractal Analytics',
    'hq': 'San Mateo, CA',

    'home_page_url': 'http://www.fractalanalytics.com',
    'jobs_page_url': 'http://www.fractalanalytics.com/content/current-openings',

    'empcnt': [501,1000],
}

class FractalAnalyticsJobScraper(JobScraper):
    def __init__(self):
        super(FractalAnalyticsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'\.pdf$')

        self.company.job_set.all().delete()

        for h5 in s.findAll('h5'):
            li = h5.findParent('li')
            a = li.find('a', href=r)
            l = self.parse_location(h5.span.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = h5.contents[0]
            job.url = a['href']
            job.location = l
            job.desc = get_all_text(li)
            job.save()

def get_scraper():
    return FractalAnalyticsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
