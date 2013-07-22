import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'SaveingStar',
    'hq': 'Waltham, MA',

    'home_page_url': 'http://savingstar.com',
    'jobs_page_url': 'http://savingstar.com/blog/savingstar-jobs/',

    'empcnt': [11,50]
}

class SaveWaveJobScraper(JobScraper):
    def __init__(self):
        super(SaveWaveJobScraper, self).__init__(COMPANY)
        
    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'entry-content'})
        x = {'style': 'font-size: xx-large; font-weight: bold;'}
        d.extract()

        self.company.job_set.all().delete()

        for p in d.findAll('span', attrs=x):
            job = Job(company=self.company)
            job.title = p.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = p.next
            while x and getattr(x, 'name', None) != 'span':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return SaveWaveJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
