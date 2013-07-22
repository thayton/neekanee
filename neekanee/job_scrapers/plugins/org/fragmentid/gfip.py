import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Global Financial Integrity',
    'hq': 'Washington, DC',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.gfip.org',
    'jobs_page_url': 'http://www.gfintegrity.org/index.php?option=com_content&task=view&id=18&Itemid=140',

    'empcnt': [11,50]
}

class GfipJobScraper(JobScraper):
    def __init__(self):
        super(GfipJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'subMain-full'})
        r = re.compile(r'^index\.php\?option=com_content')
        f = lambda x: x.name == 'strong' and x.text == 'Current Job Opportunities'
        g = d.find(f)
        t = g.findParent('table')
        d = t.findParent('div')

        self.company.job_set.all().delete()

        for a in t.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            i = a['href'].rfind('#') + 1
            x = d.find('a', attrs={'name': a['href'][i:]})
            x = x.next

            while x and getattr(x, 'name', None) != 'hr':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return GfipJobScraper()
