import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Washington College',
    'hq': 'Chestertown, MD',

    'home_page_url': 'http://www.washcoll.edu',
    'jobs_page_url': 'http://www.washcoll.edu/offices/human-resources/employment.php',

    'empcnt': [501,1000]
}

class WashCollJobScraper(JobScraper):
    def __init__(self):
        super(WashCollJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^lw_item_\d+$')
        x = {'class': r}
        y = {'class': 'lw_blurbs_title'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=y):
            li = d.findParent('li', attrs=x)
            if d != li.contents[1]:
                continue

            job = Job(company=self.company)
            job.title = d.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(li)
            job.save()

def get_scraper():
    return WashCollJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
