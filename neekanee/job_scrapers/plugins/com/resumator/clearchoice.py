import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ClearChoice',
    'hq': 'Greenwood Village, CO',

    'home_page_url': 'http://www.clearchoice.com',
    'jobs_page_url': 'http://clearchoice.theresumator.com',

    'empcnt': [501,1000]
}

class ClearChoiceJobScraper(JobScraper):
    def __init__(self):
        super(ClearChoiceJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'resumator-job-title resumator-jobs-text'}
        y = {'class': 'resumator-job-location resumator-job-heading resumator-jobs-text'}
        
        for d in s.findAll('div', attrs=x):
            d = d.findParent('div')
            p = d.find('span', attrs=y)
            l = self.parse_location(p.nextSibling)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = d.a.text
            job.url = urlparse.urljoin(self.br.geturl(), d.a['href'])
            job.location = l
            jobs.append(job)
            break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='resumator-body')
            v = d.find('div', id='resumator-content-right-wrapper')
            v.extract()

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ClearChoiceJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
