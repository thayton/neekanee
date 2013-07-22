import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, BeautifulSoup

from neekanee_solr.models import *

COMPANY = {
    'name': 'TVU networks',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.tvunetworks.com',
    'jobs_page_url': 'http://pages.tvunetworks.com/jobs/jobs_us.html',

    'empcnt': [51,200]
}

class TvuNetworksJobScraper(JobScraper):
    def __init__(self):
        super(TvuNetworksJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'textblack12'}
        td = s.find('td', attrs=x)
        x = {'class': 'style20'}

        self.company.job_set.all().delete()

        for p in td.findAll('span', attrs=x):
            job = Job(company=self.company)
            job.title = p.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = p.next
            while x:
                name = getattr(x, 'name', None)
                if name == 'span' and \
                        x.has_key('class') and x['class'] == 'style20':
                    break
                elif name is None:
                    job.desc += x
                x = x.next
            
            job.save()

def get_scraper():
    return TvuNetworksJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
