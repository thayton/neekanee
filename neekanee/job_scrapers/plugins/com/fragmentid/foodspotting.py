import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Foodspotting',
    'hq': 'San Francisco, CA',

    'contact': 'jobs@foodspotting.com',
    'benefits': {'vacation': [(1,20)]},

    'home_page_url': 'http://www.foodspotting.com',
    'jobs_page_url': 'http://www.foodspotting.com/about/jobs',

    'empcnt': [11,50]
}

class FoodSpottingJobScraper(JobScraper):
    def __init__(self):
        super(FoodSpottingJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'section job-position', 'id': True}
        d = s.find('div', id='content')

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = v.h3.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + v['id'])
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return FoodSpottingJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
