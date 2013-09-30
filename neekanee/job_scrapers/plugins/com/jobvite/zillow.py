import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Zillow',
    'hq': 'Seattle, WA',

    'home_page_url': 'http://www.zillow.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?k=JobListing&c=qVr9Vfwa&jvresize=TODO_INSERT_LINK_TO_STATICS_HERE&v=1',

    'empcnt': [501,1000]
}

class ZillowJobScraper(JobScraper):
    def __init__(self):
        super(ZillowJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/jobs/positions/\?jvi=')
        v = { 'class': 'jvlisting' }
        d = s.find('div', attrs=v)

        for a in d.findAll('a', href=r):
            p = a.findParent('li')
            l = self.parse_location(p.span.text)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
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
            x = job.url.find('jvi=')+4
            j = '&j=' + job.url[x:]
            l = s.iframe['src'] + j + '&k=Job'
            
            self.br.open(l)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'jvcontent'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ZillowJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
