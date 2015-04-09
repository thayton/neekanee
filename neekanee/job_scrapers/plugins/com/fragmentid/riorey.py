import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'RioRey',
    'hq': 'Bethesda, MD',

    'home_page_url': 'http://www.riorey.com',
    'jobs_page_url': 'http://www.riorey.com/careers',

    'empcnt': [11,50]
}

class RioReyJobScraper(JobScraper):
    def __init__(self):
        super(RioReyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'row sqs-row'}

        self.company.job_set.all().delete()

        for h2 in s.findAll('h2'):
            d = h2.findNext('div', attrs=x)
            f = lambda y: y.name == 'strong' and re.search(r'Location:', y.text)
            l = d.find(f)

            if l:
                l = l.parent.contents[-1]
                l = self.parse_location(l)

                if not l:
                    continue

            job = Job(company=self.company)
            job.title = h2.text
            job.url = self.br.geturl()
            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return RioReyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
