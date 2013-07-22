import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Historic New England',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.historicnewengland.org',
    'jobs_page_url': 'http://www.historicnewengland.org/about-us/employment',

    'empcnt': [51,200]
}

class AcusJobScraper(JobScraper):
    def __init__(self):
        super(AcusJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/about-us/employment/\S+')
        x = {'href': r, 'title': True}

        for a in s.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.company.home_page_url, a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')
            t = re.compile(r'Location:\s*')
            g = d.find('strong', text=t)
            p = g.findParent('p')
            l = self.parse_location(p.contents[-1])
            
            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return AcusJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
