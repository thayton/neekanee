import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Council on Foreign Relations',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.cfr.org',
    'jobs_page_url': 'http://www.cfr.org/about/career_opportunities/openings.html',

    'empcnt': [51,200]
}

class CfrJobScraper(JobScraper):
    def __init__(self):
        super(CfrJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#\d+')
        d = s.find('div', id='container')

        self.company.job_set.all().delete()

        locations = {'New York': self.parse_location('New York, NY'), 
                     'Washington': self.parse_location('Washington, DC')} 

        for k in locations.keys():
            for h2 in d.findAll('h2', text=k):
                ul = h2.findNext('ul')

                for a in ul.findAll('a', href=r):
                    if not locations[k]:
                        continue

                    job = Job(company=self.company)
                    job.title = a.text
                    job.location = locations[k]
                    job.url = urlparse.urljoin(self.br.geturl(), a['href'])

                    x = d.find('a', id=a['href'][1:])

                    if not x:
                        continue

                    x = x.findNext('div', attrs={'class': 'job-spotlight'})

                    job.desc = get_all_text(x)
                    job.save()

def get_scraper():
    return CfrJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
