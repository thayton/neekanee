import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Nasuni',
    'hq': 'Natick, MA',

    'contact': 'jobs@nasuni.com',

    'home_page_url': 'http://www.nasuni.com',
    'jobs_page_url': 'http://www.nasuni.com/about/careers',

    'empcnt': [11,50]
}

class NasuniJobScraper(JobScraper):
    def __init__(self):
        super(NasuniJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'main'})
        r = re.compile(r'^#')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find(id=a['href'][1:])
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
    return NasuniJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
