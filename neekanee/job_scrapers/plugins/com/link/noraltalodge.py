import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Noralta Lodge',
    'hq': 'Nisku, Canada',

    'home_page_url': 'http://www.noraltalodge.com',
    'jobs_page_url': 'http://www.noraltalodge.com/index.php?option=com_content&view=category&layout=blog&id=35&Itemid=53',

    'empcnt': [501,1000]
}

class NoraltaLodgeJobScraper(JobScraper):
    def __init__(self):
        super(NoraltaLodgeJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'index\.php\?')
        x = {'href': r, 'title': 'PDF', 'onclick': True}

        self.company.job_set.all().delete()

        # Skip the first one, it's not really a job description
        y = s.findAll('a', attrs=x)

        for a in y[1:]:
            d = a.parent.parent
            job = Job(company=self.company)
            job.title = d.h2.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.save()

def get_scraper():
    return NoraltaLodgeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
