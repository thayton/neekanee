import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ozmosis',
    'hq': 'Washington, DC',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.ozmosis.com',
    'jobs_page_url': 'http://ozmosis.com/about-us/careers/',

    'empcnt': [1,10]
}

class OzmosisJobScraper(JobScraper):
    def __init__(self):
        super(OzmosisJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#career-\d+')
        u = s.find('ul', id='careers-selector')
        d = u.findParent('div').findParent('div')
        x = {'rel': r}
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            v = d.find('div', id=a['rel'][1:])
        
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return OzmosisJobScraper()
