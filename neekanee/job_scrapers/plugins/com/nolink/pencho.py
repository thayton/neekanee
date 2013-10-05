import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Pencho',
    'hq': 'Beijing, China',

    'home_page_url': 'http://www.pencho.com.cn',
    'jobs_page_url': 'http://www.pencho.com.cn/sixth_en.html',

    'empcnt': [11,50]
}

class PenchoJobScraper(JobScraper):
    def __init__(self):
        super(PenchoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'title_en'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            v = d.parent.parent
            job = Job(company=self.company)
            job.title = d.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return PenchoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
