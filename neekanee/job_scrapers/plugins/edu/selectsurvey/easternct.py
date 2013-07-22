import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Eastern Connecticut State University',
    'hq': 'Willimantic, CT',

    'ats': 'SelectSurvey',

    'home_page_url': 'http://www.easternct.edu',
    'jobs_page_url': 'http://www.easternct.edu/humanresources/admin.html',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

class EasternCtJobScraper(JobScraper):
    def __init__(self):
        super(EasternCtJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')

        self.company.job_set.all().delete()

        # Only administrative positions (no faculty) are done
        for a in s.findAll('a', href=r):
            if a['href'] == '#top':
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = s.find(attrs={'name' : a['href'][1:]})        
            while x and getattr(x, 'name', None) != 'hr':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.desc = job.desc.replace('&nbsp;', '')
            job.save()

def get_scraper():
    return EasternCtJobScraper()
