import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Message Systems',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://messagesystems.com',
    'jobs_page_url': 'http://messagesystems.com/about-us/careers/open-positions',

    'empcnt': [51,200]
}

class MessageSystemsJobScraper(JobScraper):
    def __init__(self):
        super(MessageSystemsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/careers/open-positions/[^/]+$')
        
        for a in s.findAll('a', href=r):
            x = {'class': 'field-content'}
            p = a.findNext('span', attrs=x)
            l = self.parse_location(p.text)
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
            r = re.compile(r'^node-employment-position-\d+$')
            a = s.find('article', id=r)

            job.desc = get_all_text(a)
            job.save()

def get_scraper():
    return MessageSystemsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
