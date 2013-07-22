import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'StreetAccount',
    'hq': 'Boston, MA',

    'contact': 'employment@streetaccount.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.streetaccount.com',
    'jobs_page_url': 'https://www.streetaccount.com/careers.aspx',

    'empcnt': [11,50]
}

class StreetAccountJobScraper(JobScraper):
    def __init__(self):
        super(StreetAccountJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        x = {'class': 'mainLoggedOutLinks', 'href': r}
        t = s.find(text='Careers')
        d = t.findParent('div')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', attrs=x):
            m = re.search(r'\((.*)\)', a.nextSibling)
            l = self.parse_location(m.group(1))

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            job.desc = ''

            x = d.find(attrs={'name' : a['href'][1:]})
            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'a' and x.has_key('name'):
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return StreetAccountJobScraper()
