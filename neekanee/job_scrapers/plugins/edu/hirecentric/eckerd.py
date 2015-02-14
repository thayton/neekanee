import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Eckerd College',
    'hq': 'St. Petersburg, FL',

    'home_page_url': 'http://www.eckerd.edu',
    'jobs_page_url': 'http://eckerd.hirecentric.com/jobs/',

    'empcnt': [201,500]
}

class EckerdJobScraper(JobScraper):
    def __init__(self):
        super(EckerdJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', id='job_listing')
        r = re.compile(r'^/jobs/\d+\.html$')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-1].text)
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
            x = {'class': 'job_info'}
            d = s.find('div', attrs=x)
            d = d.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return EckerdJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
