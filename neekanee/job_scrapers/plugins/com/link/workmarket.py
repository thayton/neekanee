import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Work Market',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.workmarket.com',
    'jobs_page_url': 'https://www.workmarket.com/ats/index',

    'empcnt': [11,50]
}

class WorkMarketJobScraper(JobScraper):
    def __init__(self):
        super(WorkMarketJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/ats/view\?id=\d+$')
        d = s.find('div', id='current-careers')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'content topcontent'}
            d = s.find('div', attrs=x)
            f = lambda x: x.name == 'b' and x.text == 'Location'
            b = d.find(f)
            l = b.parent.contents[-1].split(':')[1]
            l = self.parse_location(l)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WorkMarketJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

