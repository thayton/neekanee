import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ScanScout',
    'hq': 'Boston, MA',

    'contact': 'careers@scanscout.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.scanscout.com',
    'jobs_page_url': 'http://www.scanscout.com/about_careers.php#careers-00006',

    'empcnt': [11,50]
}

class ScanScoutJobScraper(JobScraper):
    def __init__(self):
        super(ScanScoutJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'#careers-\d+')
        v = { 'class': 'joblink', 'href': r }
        d = s.find('div', id='content_wide_left')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', attrs=v):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find(attrs={'name' : a['href'][1:]})
            x = x.next

            l = x.findNext(text='Location:').next
            l = self.parse_location(l)

            if l is None:
                continue

            job.location = l

            while x:
                if hasattr(x, 'name') is False: 
                    job.desc += x
                elif x.name == 'br' and x.has_key('clear'):
                    break
                x = x.next

            job.save()

def get_scraper():
    return ScanScoutJobScraper()
