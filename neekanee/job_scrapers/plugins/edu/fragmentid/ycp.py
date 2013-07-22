import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'York College of Pennsylvania',
    'hq': 'York, PA',

    'home_page_url': 'http://www.ycp.edu',
    'jobs_page_url': 'http://www.ycp.edu/offices-and-services/human-resources/employment-opportunities/',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

class YcpJobScraper(JobScraper):
    def __init__(self):
        super(YcpJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/human-resources/employment-opportunities/\w+-opportunities/$')
        x = {'class': 'secondary-nav text-shadow'}
        d = s.find('div', attrs=x)

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            link = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(link)

            x = soupify(self.br.response().read())
            v = x.find('div', attrs={'class': 'main group'})

            for l in v.findAll('a', href=re.compile(r'#')):
                if l['href'] == '#top':
                    continue

                job = Job(company=self.company)
                job.title = l.text
                job.url = urlparse.urljoin(self.br.geturl(), l['href'])
                job.location = self.company.location

                i = l['href'].find('#') + 1
                x = v.find(attrs={'name' : l['href'][i:]})
                q = x.findParent('div', attrs={'class': 'section lower'})

                job.desc = get_all_text(q)
                job.save()

def get_scraper():
    return YcpJobScraper()
