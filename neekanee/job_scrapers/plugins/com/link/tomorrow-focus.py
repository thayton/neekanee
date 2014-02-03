import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tomorrow Focus',
    'hq': 'Munich, Germany',

    'home_page_url': 'http://www.tomorrow-focus.com',
    'jobs_page_url': 'http://www.tomorrow-focus.com/jobs-careers/jobs/',

    'empcnt': [501,1000]
}

class TomorrowFocusJobScraper(JobScraper):
    def __init__(self):
        super(TomorrowFocusJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobrow'}
        
        for tr in s.findAll('tr', attrs=x):
            td = tr.findAll('td')
            l = self.parse_location(td[-2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = tr.a.text
            job.url = urlparse.urljoin(self.br.geturl(), tr.a['href'])
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
            x = {'class': 'area jobDetail'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TomorrowFocusJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
