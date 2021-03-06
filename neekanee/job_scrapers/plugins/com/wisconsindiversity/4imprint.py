import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': '4imprint',
    'hq': 'Oshkosh, WI',

    'home_page_url': 'http://www.4imprint.com',
    'jobs_page_url': 'http://www.wisconsindiversity.com/jobs.asp?pbid=67775',

    'empcnt': [51,200]
}

class FourImprintJobScraper(JobScraper):
    def __init__(self):
        super(FourImprintJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r"javascript:self\.popup\('([^']+)")

        for a in s.findAll('a', href=r):
            m = re.search(r, a['href'])

            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = m.group(1)
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
            x = {'itemprop': 'description'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return FourImprintJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
