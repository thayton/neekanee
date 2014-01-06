import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Deerfield Academy',
    'hq': 'Springfield, MA',

    'home_page_url': 'http://deerfield.edu',
    'jobs_page_url': 'http://deerfield.edu/heritage/people/faculty-staff/working-at-deerfield/staff-employment/',

    'empcnt': [51,200]
}

class DeerfieldJobScraper(JobScraper):
    def __init__(self):
        super(DeerfieldJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h2' and x.text == 'Current Openings'
        h = s.find(f)
        u = h.findNext('ul')
        r = re.compile(r'/working-at-deerfield/')

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='colContent')
            x = {'class': re.compile(r'entry_content')}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DeerfieldJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
