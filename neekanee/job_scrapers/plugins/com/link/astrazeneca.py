import re, urlparse, mechanize, urllib2

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'AstraZeneca',
    'hq': 'London, England',

    'home_page_url': 'http://www.astrazeneca.com',
    'jobs_page_url': 'http://jobs.astrazeneca.com/jobs/result',

    'empcnt': [10001]
}

class AstraZenecaJobScraper(JobScraper):
    def __init__(self):
        super(AstraZenecaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        r1 = re.compile(r'/jobs/location/([^/]+)')
        r2 = re.compile(r'/jobs/country/([^/]+)')

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'/jobs/details/')
            x = {'class': 'job-title', 'href': r}

            for a in s.findAll('a', attrs=x):
                d = a.findParent('div')

                l1 = d.ul.find('a', href=r1)
                l2 = d.ul.find('a', href=r2)

                m1 = re.search(r1, l1['href']) 
                m2 = re.search(r2, l2['href'])

                l = m1.group(1) + ', ' + m2.group(1)
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = urllib2.quote(job.url, '/:?&=,')
                job.location = self.company.location
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'az-joblisting'}
            h = s.find('h1', attrs=x)
            d = h.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return AstraZenecaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
