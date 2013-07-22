import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'CarGurus',
    'hq': 'Cambridge, MA',

    'contact': 'jobs@cargurus.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.cargurus.com',
    'jobs_page_url': 'http://www.cargurus.com/Cars/jobs.html',

    'empcnt': [1,10]
}

class CarGurusJobScraper(JobScraper):
    def __init__(self):
        super(CarGurusJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='contentBody')
        r = re.compile(r'^#')

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            x = s.find(attrs={'name' : a['href'][1:]})
            d = x.findNext('div')
        
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CarGurusJobScraper()
