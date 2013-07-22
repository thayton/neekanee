import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Daytona State College',
    'hq': 'Daytona Beach, FL',

    'home_page_url': 'http://www.daytonastate.edu',
    'jobs_page_url': 'http://www.daytonastate.edu/hr/',

    'empcnt': [1001,5000]
}

class DaytonaStateJobScraper(JobScraper):
    def __init__(self):
        super(DaytonaStateJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'^/hr/\S+\.html$')

        for a in d.findAll('a', href=r):
            u = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(u)

            x = soupify(self.br.response().read())
            v = x.find('div', id='content')

            for a in v.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])

                if job.url.find(' ') != -1:
                    job.url = urllib.quote(job.url, '/:')

                job.location = self.company.location
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in job_list:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')

            if not d:
                x = {'class': 'rightbody2'}
                d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DaytonaStateJobScraper()
