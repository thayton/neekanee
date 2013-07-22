import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Botify',
    'hq': 'Paris, France',

    'home_page_url': 'http://www.botify.com',
    'jobs_page_url': 'http://www.botify.com/jobs/',

    'empcnt': [1,10]
}

class BotifyJobScraper(JobScraper):
    def __init__(self):
        super(BotifyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='page_content')
        x = {'class': 'paragraph', 'id': True}
        d.extract()

        self.company.job_set.all().delete()

        for n in d.findAll('section', attrs=x):
            if n['id'] == 'our-company':
                continue

            job = Job(company=self.company)
            job.title = n.h4.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + n['id'])
            job.location = self.company.location
            job.desc = ''
            
            y = n.next
            
            while y:
                name = getattr(y, 'name', None)
                if name == 'section' and y.get('id', None):
                    break
                elif name is None:
                    job.desc += y
                y = y.next

            job.save()

def get_scraper():
    return BotifyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
