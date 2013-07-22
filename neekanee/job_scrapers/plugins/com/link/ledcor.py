import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ledcor',
    'hq': 'Vancouver, Canada',

    'home_page_url': 'http://www.ledcor.com',
    'jobs_page_url': 'http://www.ledcor.com/careers/search-careers',

    'empcnt': [10001]
}

class LedcorJobScraper(JobScraper):
    def __init__(self):
        super(LedcorJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r'^/job\?id=\d+$')

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='job-search-list')

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[1].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            a = s.find('article', id='content-body')

            job.desc = get_all_text(a)
            job.save()

def get_scraper():
    return LedcorJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
