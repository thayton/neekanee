import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Internet Archive',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.archive.org',
    'jobs_page_url': 'http://www.archive.org/about/jobs.php',

    'empcnt': [51,200]
}

class ArchiveJobScraper(JobScraper):
    def __init__(self):
        super(ArchiveJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='col2')
        d = d.find('div', attrs={'class': 'box'})
        x = {'name': True}
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + a['name'])
            job.location = self.company.location
            job.desc = ''

            x = a.findNext('h2')
            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h2':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return ArchiveJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
