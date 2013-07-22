import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'iFeelGoods',
    'hq': 'Menlo Park, CA',

    'home_page_url': 'http://www.ifeelgoods.com',
    'jobs_page_url': 'http://www.ifeelgoods.com/about-us/careers/',

    'empcnt': [1,10]
}

class IFeelGoodsJobScraper(JobScraper):
    def __init__(self):
        super(IFeelGoodsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content-part')
        x = {'class': 'toggle'}

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            z = v.findParent('div')
            t = v.find('div', attrs={'class': 'title'})

            job = Job(company=self.company)
            job.title = t.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + z['id'])

            l = self.parse_location(v.h4.text)
            if not l:
                continue

            job.location = l
            job.desc = get_all_text(z)
            job.save()

def get_scraper():
    return IFeelGoodsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
