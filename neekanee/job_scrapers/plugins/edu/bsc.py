import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Birmingham-Southern College',
    'hq': 'Birmingham, AL',

    'benefits': {
        'url': 'http://www.bsc.edu/administration/humanresources/benefits.cfm',
        'vacation': [(0,12),(4,18),(16,24)],
        'holidays': 9,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.bsc.edu',
    'jobs_page_url': 'http://www.bsc.edu/administration/humanresources/job_opportunities.cfm',

    'empcnt': [201,500]
}

class BscJobScraper(JobScraper):
    def __init__(self):
        super(BscJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^job_descriptions')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            link,frag = urlparse.urldefrag(job.url)
            self.br.open(link)

            s = soupify(self.br.response().read())
            a = s.find('a', id=frag)
            d = a.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BscJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
