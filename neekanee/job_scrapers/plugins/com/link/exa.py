import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Exa Corporation',
    'hq': 'Burlington, MA',

    'home_page_url': 'http://exa.com',
    'jobs_page_url': 'http://exa.com/careers.html',

    'empcnt': [201,500]
}

class ExaJobScraper(JobScraper):
    def __init__(self):
        super(ExaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='u11684-135')
        r = re.compile(r'\.html$')
        f = lambda x: x.name == 'a' and x.parent.name == 'p' and re.search(r, x['href'])
        
        for a in d.findAll(f):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('h1').parent
            f = lambda x: x.name == 'h2' and x.text == 'LOCATION:'
            l = s.find(f)

            if not l:
                continue

            p = l.findNext('p')
            l = self.parse_location(p.text)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ExaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
