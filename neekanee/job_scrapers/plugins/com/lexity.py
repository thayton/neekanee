import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lexity',
    'hq': 'Mountain View, CA',

    'contact': 'jobs@lexity.com',

    'home_page_url': 'http://lexity.com',
    'jobs_page_url': 'http://lexity.com/about/jobs',

    'empcnt': [11,50]
}

class VurveJobScraper(JobScraper):
    def __init__(self):
        super(VurveJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='page_content')
        w = re.compile(r'well')
        x = {'class': w}
        d.extract()

        self.company.job_set.all().delete()

        for div in d.findAll('div', attrs=x):
            h3 = div.findPrevious('h3')
            h3 = h3.text.lower()

            l = None
            if h3.find('mountain view') != -1:
                l = self.parse_location('Mountain View, CA')
            elif h3.find('bangalore') != -1:
                l = self.parse_location('Bangalore, India')
            else:
                continue

            job = Job(company=self.company)
            job.title = div.h4.text
            job.url = self.br.geturl()
            job.location = l
            job.desc = get_all_text(div)
            job.save()

def get_scraper():
    return VurveJobScraper()
