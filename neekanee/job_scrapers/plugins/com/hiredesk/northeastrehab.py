import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Northeast Rehabilitation Network',
    'hq': 'Salem, NH',

    'home_page_url': 'http://www.northeastrehab.com',
    'jobs_page_url': 'http://careers2.hiredesk.net/Welcome/Default.asp?Comp=NorthEastRehab&AN=en-US',

    'empcnt': [501,1000]
}

class NortheastRehabJobScraper(JobScraper):
    def __init__(self):
        super(NortheastRehabJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='TPMainContentDiv')
        r = re.compile(r'^/viewjobs/JobDetail\.asp\?')

        for a in d.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[-3].text + ', ' + td[-2].text
            l = self.parse_location(l)

            if not l:
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
            d = s.find('div', id='TPMainContentDiv')
            x = {'class': 'FormContent'}
            t = d.find('table', attrs=x)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return NortheastRehabJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
