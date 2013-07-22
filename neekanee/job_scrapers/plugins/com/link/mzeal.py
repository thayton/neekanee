import re, urllib2, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'mZeal',
    'hq': 'Fitchburg, MA',

    'home_page_url': 'http://www.mzeal.com',
    'jobs_page_url': 'http://www.mzeal.com/htdocs/mzeal-careers.php',

    'empcnt': [11,50]
}

class mZealJobScraper(JobScraper):
    def __init__(self):
        super(mZealJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'^javascript:popUp\("([^"]+)')

        for a in d.findAll('a', href=r):
            m = re.search(r, a['href'])
            u = urllib2.quote(m.group(1))

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), u)
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
            d = s.div

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return mZealJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
