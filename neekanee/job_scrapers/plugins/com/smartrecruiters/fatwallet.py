import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Fat Wallet',
    'hq': 'Rockton, IL',

    'home_page_url': 'http://www.fatwallet.com',
    'jobs_page_url': 'https://careers.smartrecruiters.com/EbatesShoppingcomInc',

    'empcnt': [51,200]
}

class FatWalletJobScraper(JobScraper):
    def __init__(self):
        super(FatWalletJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'\job-title\b')
        x = {'class': r}

        for h3 in s.findAll('h3', attrs=x):
            job = Job(company=self.company)
            job.title = h3.text
            job.url = urlparse.urljoin(self.br.geturl(), h3.parent['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            m = s.main

            x = {'itemprop': 'address'}
            p = m.find('span', attrs=x)
            l = self.parse_location(p.text)

            if not l:
                continue

            job.desc = get_all_text(m)
            job.save()

def get_scraper():
    return FatWalletJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
