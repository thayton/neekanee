import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'iFeelGoods',
    'hq': 'Menlo Park, CA',

    'home_page_url': 'http://www.ifeelgoods.com',
    'jobs_page_url': 'http://www.ifeelgoods.com/careers/',

    'empcnt': [1,10]
}

class IFeelGoodsJobScraper(JobScraper):
    def __init__(self):
        super(IFeelGoodsJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'spb_toggle'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            l = d.text.split('-')[1]
            l = self.parse_location(l)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = d.text
            job.url = self.br.geturl()
            job.location = l
            job.desc = get_all_text(d.parent)
            job.save()

def get_scraper():
    return IFeelGoodsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
