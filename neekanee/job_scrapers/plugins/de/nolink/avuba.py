import re, urlparse, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from doctohtml import doctohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Avuba GmbH',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.avuba.de',
    'jobs_page_url': 'https://cdn.contentful.com/spaces/90xvvflgedhc/entries?access_token=73e6f5b084822947bcbb5e281e989644fb2c321768eb82b93015d4a34360b233&content_type=58J6Ld4U7eC0owYUwkY4u2&locale=en',

    'empcnt': [1,10]
}

class AvubaJobScraper(JobScraper):
    def __init__(self):
        super(AvubaJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)
        
        r = self.br.response()
        j = json.loads(r.read())

        self.company.job_set.all().delete()

        for i in j['items']:
            f = i['fields']
            s = soupify(f['body'])

            job = Job(company=self.company)
            job.title = f['title']
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(s)
            job.save()

def get_scraper():
    return AvubaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
