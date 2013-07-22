import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Westminster College',
    'hq': 'Salt Lake City, UT',

    'home_page_url': 'http://www.westminstercollege.edu',
    'jobs_page_url': 'https://jobs.westminstercollege.edu/postings/search',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class WestminsterCollegeJobScraper(JobScraper):
    def __init__(self):
        super(WestminsterCollegeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', attrs={'class': 'NEOGOV_joblist'})
        r = re.compile(r'default\.cfm\?action=viewJob&jobID=\d+')

        for a in t.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = url_query_filter(job.url, ['action', 'jobID'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'jobdetail', 'headers': 'viewJobDescription'}
            t = s.find('td', attrs=x)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return WestminsterCollegeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
