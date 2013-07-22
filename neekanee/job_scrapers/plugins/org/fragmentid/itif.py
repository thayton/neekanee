import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Information Technology and Innovation Foundation',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.itif.org',
    'jobs_page_url': 'http://www.itif.org/content/jobs',

    'empcnt': [1,10]
}

class ItifJobScraper(JobScraper):
    def __init__(self):
        super(ItifJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content-area')
        d = d.find('div', attrs={'class': 'content'})
        r = re.compile(r'^#')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ' '

            y = a['href'][1:]
            x = d.find(attrs={'name' : y})

            while x:
                name = getattr(x, 'name', None)
                if name == 'span' and \
                        x.get('style') == 'font-size: large;':
                    break
                elif name is None:
                    job.desc += x + ' '
                x = x.next

            job.save()

def get_scraper():
    return ItifJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
