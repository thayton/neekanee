import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Booking.com',
    'hq': 'Amsterdam, Netherlands',

    'home_page_url': 'http://www.booking.com',
    'jobs_page_url': 'http://www.booking.com/jobs.html?st=top',

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
        self.br.follow_link(self.br.find_link(text='See all jobs'))

        s = soupify(self.br.response().read())
        x = {'class': 'countries'}
        u = s.find('ul', attrs=x)
        r = re.compile(r'country=[a-z]{2}')
        
        for a in u.findAll('a', href=r):
            country = a.text

            u = urlparse.urljoin(self.br.geturl(), a['href'])

            self.br.open(u)

            x = soupify(self.br.response().read())
            d = x.find('div', id='jobsTmpl')
            z = re.compile(r'job_id=\d+')

            for a in d.findAll('a', href=z):
                p = a.parent.span
                l = p.text.rsplit('-', 1)
                l = l[1] + ', ' + country
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = urlutil.url_query_del(job.url, 'sid')
                job.location = l
                jobs.append(job)

            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='job_detail')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BookingJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
