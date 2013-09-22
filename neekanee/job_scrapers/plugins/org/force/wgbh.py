import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'WGBH',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.wgbh.org',
    'jobs_page_url': 'https://wgbh.secure.force.com/openpositions',

    'empcnt': [501,1000]
}

class WgbhJobScraper(JobScraper):
    def __init__(self):
        super(WgbhJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/positiondetail\?id=\w+$')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            if a.parent != td[1]:
                continue

            l = self.parse_location(td[-2].text)
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
            x = {'class': 'positionDetailSurround'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WgbhJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
