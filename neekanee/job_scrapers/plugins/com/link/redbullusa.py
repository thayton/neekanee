import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Red Bull USA',
    'hq': 'Fuschl am See, Austria',

    'home_page_url': 'http://www.redbullusa.com',
    'jobs_page_url': 'http://jobs.redbull.com/us/en-US/results',

    'empcnt': [5001,10000]
}

class RedBullUsaJobScraper(JobScraper):
    def __init__(self):
        super(RedBullUsaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'result-link'}
            y = {'itemprop': 'jobLocation'}
        
            for a in s.findAll('a', attrs=x):
                p = a.find('span', attrs=y)
                l = self.parse_location(p.text)
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
            x = {'class': re.compile(r'job'), 'itemtype': True}
            n = s.find('section', attrs=x)

            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return RedBullUsaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
