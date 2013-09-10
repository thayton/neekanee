import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Rethink Robotics',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.rethinkrobotics.com',
    'jobs_page_url': 'http://www.rethinkrobotics.com/index.php/about/careers/',

    'empcnt': [51,200]
}

class RethinkRoboticsJobScraper(JobScraper):
    def __init__(self):
        super(RethinkRoboticsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'careers'}
        d = s.find('div', attrs=x)
        r = re.compile(r'/about/careers/posting/')

        for a in d.findAll('a', href=r):
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
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'page-title'}
            h = s.find('h1', attrs=x)
            n = h.parent

            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return RethinkRoboticsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
