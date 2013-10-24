import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Core Security',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.coresecurity.com',
    'jobs_page_url': 'http://www.coresecurity.com/grid/careers',

    'empcnt': [51,200]
}

class CoreSecurityJobScraper(JobScraper):
    def __init__(self):
        super(CoreSecurityJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': re.compile(r'\bview-id-careers\b')}
        d = s.find('div', attrs=x)
        y = {'class': re.compile(r'views-field-title')}
        z = {'class': re.compile(r'views-field-field-office-location')}

        for td in d.findAll('td', attrs=y):
            tr = td.findParent('tr')
            l = tr.find('td', attrs=z)

            if len(l.text.strip()) == 0:
                continue

            l = self.parse_location(l.text)

            if not l:
                continue 

            job = Job(company=self.company)
            job.title = td.a.text
            job.url = urlparse.urljoin(self.br.geturl(), td.a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)
            
            s = soupify(self.br.response().read())
            n = s.find('section', id='section-content')

            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return CoreSecurityJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
