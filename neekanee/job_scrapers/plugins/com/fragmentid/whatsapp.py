import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'WhatsApp',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.whatsapp.com',
    'jobs_page_url': 'http://www.whatsapp.com/join/',

    'empcnt': [1,10]
}

class WhatsAppJobScraper(JobScraper):
    def __init__(self):
        super(WhatsAppJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'body join'})
        d.extract()

        self.company.job_set.all().delete()

        for h3 in d.findAll('h3'):
            if h3.text.lower().find('why come here') != -1:
                continue

            job = Job(company=self.company)
            job.title = h3.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + h3['id'])
            job.location = self.company.location
            job.desc = ''

            x = h3.next
            while x:
                name = getattr(x, 'name', None)
                if name == 'h3':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return WhatsAppJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
