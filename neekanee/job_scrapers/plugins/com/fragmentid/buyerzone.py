import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BuyerZone',
    'hq': 'Waltham, MA',

    'contact': 'jobs@buyerzone.com',
    'benefits': {
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.buyerzone.com',
    'jobs_page_url': 'http://www.buyerzone.com/pages/about/careers.html',

    'empcnt': [51,200]
}

class BuyerZoneJobScraper(JobScraper):
    def __init__(self):
        super(BuyerZoneJobScraper, self).__init__(COMPANY)
        
    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='careers')
        r = re.compile(r'^#')

        self.company.job_set.all().delete()

        for a in d.ul.findAll('a', href=r):
            v = s.find('div', id='career-descriptions')
            x = v.find('div', id=a['href'][1:])
            e = x.find('a', href=re.compile(r'\w+@'))

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.desc = get_all_text(x)
            job.location = self.company.location
            job.save()

def get_scraper():
    return BuyerZoneJobScraper()
