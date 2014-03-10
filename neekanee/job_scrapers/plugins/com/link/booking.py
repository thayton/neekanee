import re, urlparse, urlutil, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Booking.com',
    'hq': 'Amsterdam, Netherlands',

    'home_page_url': 'http://www.booking.com',
    'jobs_page_url': 'https://workingatbooking.com/vacancies/',

    'empcnt': [1001,5000]
}

class BookingJobScraper(JobScraper):
    def __init__(self):
        super(BookingJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'article-title'}

            for h in s.findAll('h3', attrs=x):
                a = h.findParent('article')
                
                job = Job(company=self.company)
                job.title = a.h3.text
                job.url = urlparse.urljoin(self.br.geturl(), a.a['href'])
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
            n = s.find('section', id='vacancy-header')
            x = {'class': 'location'}
            h = n.find('h2', attrs=x)
            l = self.parse_location(h.text)

            if not l:
                continue

            job.desc = get_all_text(n.parent)
            job.save()

def get_scraper():
    return BookingJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
