import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_add

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tenable Network Security',
    'hq': 'Columbia, MD',

    'home_page_url': 'http://www.tenable.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qmr9VfwB&jvprefix=http%3a%2f%2fwww.tenable.com&jvresize=http%3a%2f%2ftenable.com%2fjobvite.html&k=JobListing&v=1',

    'empcnt': [51,200]
}

class TenableSecurityJobScraper(JobScraper):
    def __init__(self):
        super(TenableSecurityJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'joblist'}
        u = s.find('ul', attrs=x)
        r = re.compile(r'jvi=(.*)$')
        
        for a in u.findAll('a', href=r):
            l = a.parent.span
            l = self.parse_location(l.text)

            if not l:
                continue

            m = re.search(r, a['href'])
            jobid = m.group(1)

            job = Job(company=self.company)
            job.title = a.text
            job.url = url_query_add(self.br.geturl(), {'j': m.group(1)}.items())
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
            f = s.find('form', attrs={'name': 'jvform'})

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return TenableSecurityJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
