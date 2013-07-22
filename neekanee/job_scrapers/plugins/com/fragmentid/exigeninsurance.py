import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Exigen Insurance Solutions',
    'hq': 'San Francisco, CA',

    'contact': 'kjohnson@exigeninsurance.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.exigeninsurance.com',
    'jobs_page_url': 'http://www.exigeninsurance.com/about/jobs.html',

    'empcnt': [201,500]
}

class ExigenJobScraper(JobScraper):
    def __init__(self):
        super(ExigenJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        d = s.find('div', id='ContentChannel')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.ul.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find('a', attrs={'name' : a['href'][1:]})
            l = x.findNext(text='Work Location')
            l = l.findNext('p').text
            l = self.parse_location(l)

            if not l:
                continue

            stop = x.findNext('a', attrs={'name':True})
            while x and x != stop:
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next
        
            job.location = l
            job.save()

def get_scraper():
    return ExigenJobScraper()
