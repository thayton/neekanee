import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vertica Systems',
    'hq': 'Billerica, MA',

    'contact': 'resumes@vertica.com',

    'home_page_url': 'http://www.vertica.com',
    'jobs_page_url': 'http://www.vertica.com/about/careers/',

    'empcnt': [51,200]
}

class VerticaJobScraper(JobScraper):
    def __init__(self):
        super(VerticaJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'post-\d+$')
        x = {'class': 'careers-list'}
        d = s.find('div', attrs=x)
        d.extract()

        self.company.job_set.all().delete()

        for dt in d.findAll('dt', id=r):
            dl = dt.findParent('dl')
            dd = dl.find('dd')

            job = Job(company=self.company)
            job.title = dt.text
            job.url = urlparse.urljoin(self.br.geturl(), dt.a['href'])
            job.location = self.company.location
            job.desc = get_all_text(dd)
            job.save()

def get_scraper():
    return VerticaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
