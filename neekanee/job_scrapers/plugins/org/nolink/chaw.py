import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Capitol Hill Arts Workshop',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.chaw.org',
    'jobs_page_url': 'http://chaw.org/index.php/about_us/Employment_Opportunities/',

    'empcnt': [11,50]
}

class ChawJobScraper(JobScraper):
    def __init__(self):
        super(ChawJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [ ('Connection', 'keep-alive'),
                               ('Cache-Control', 'max-age=0'),
                               ('User-agent', 
                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7'),
                               ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                               ('Referer', 'http://www.chaw.org/'),]

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='basic_content')
        d.extract()

        self.company.job_set.all().delete()

        for h2 in [ h2 for h2 in d.findAll('h2') if h2.text != '' ]:
            job = Job(company=self.company)
            job.title = h2.text
            job.url = self.br.geturl()
            job.company
            job.location = self.company.location
            job.desc = ''

            x = h2.next

            while x and getattr(x, 'name', None) != 'h2':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return ChawJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
