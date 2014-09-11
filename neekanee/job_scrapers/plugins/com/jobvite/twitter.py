import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_get

from neekanee_solr.models import *

COMPANY = {
    'name': 'Twitter',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.twitter.com',
    'jobs_page_url': 'https://hire.jobvite.com/CompanyJobs/Careers.aspx?c=q8o9Vfwk',

    'empcnt': [1001,5000]
}

class AiryLabsJobScraper(JobScraper):
    def __init__(self):
        super(AiryLabsJobScraper, self).__init__(COMPANY)

    def new_url(self, url, jvi):
        u = urlparse.urlparse(url)
        l = urlparse.parse_qsl(u.query)
        x = [ (k,v) for (k,v) in l if k == 'c' ]

        x.append(('page', 'Job Description'))
        x.append(('j',     jobid))

        u = list(u)
        u[4] = urllib.urlencode(x)
        u = urlparse.urlunparse(u)

        return u

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-listing'}
        d = s.find('div', attrs=x)
        y = {'class': 'job-location'}

        for z in d.findAll('div', attrs=y):
            l = self.parse_location(z.text)
            if not l:
                continue

            ul = z.findNext('ul')

            for a in ul.findAll('a'):
                job = Job(company=self.company)
                job.title = a.text
                job.url = a['href']
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
            i = s.iframe['src']

            self.br.open(s.iframe['src'])

            s = soupify(self.br.response().read())
            f = s.find('form', id='jvform')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return AiryLabsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
