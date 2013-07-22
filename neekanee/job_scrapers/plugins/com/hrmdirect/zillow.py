import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Zillow',
    'hq': 'Seattle, WA',

    'ats': 'hrm direct',

    'home_page_url': 'http://www.zillow.com',
    'jobs_page_url': 'http://zillow.hrmdirect.com/employment/job-openings.php',

    'empcnt': [501,1000]
}

class ZillowJobScraper(JobScraper):
    def __init__(self):
        super(ZillowJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('searchReqs')
        self.br.submit()

        s = soupify(self.br.response().read())
        x = {'class': 'reqResult'}
        d = s.find('div', attrs=x)
        z = {'class': 'jobListItem'}

        for v in d.findAll('div', attrs=z):
            y = {'class': 'jobListLocation'}
            l = v.findAll('span', attrs=y)
            l = self.parse_location(l[-1].contents[-1])

            if not l:
                continue

            job = Job(company=self.company)
            job.title = v.a.text
            job.url = urlparse.urljoin(self.br.geturl(), v.a['href'])
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
            x = {'class': 'reqResult'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ZillowJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
