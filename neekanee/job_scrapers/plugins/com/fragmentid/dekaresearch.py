import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'DEKA research',
    'hq': 'Manchester, NH',

    'home_page_url': 'http://www.dekaresearch.com',
    'jobs_page_url': 'http://www.dekaresearch.com/careers.shtml',

    'empcnt': [51,200]
}

class DekaResearchJobScraper(JobScraper):
    def __init__(self):
        super(DekaResearchJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='text_box')
        r = re.compile(r'^#\S+')
        x = {'class': 'job_post'}
        v = s.find('div', attrs=x)
        v.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''
            
            x = v.find('a', attrs={'name' : a['href'][1:]})
            if not x:
                continue

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
    return DekaResearchJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
