import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Netsertive',
    'hq': 'Research Triangle Park, NC',

    'home_page_url': 'http://www.netsertive.com',
    'jobs_page_url': 'http://www.netsertive.com/careers',

    'empcnt': [11,50]
}

class NetsertiveJobScraper(JobScraper):
    def __init__(self):
        super(NetsertiveJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'entry-content article'}
        d = s.find('div', attrs=x)
        r = re.compile(r'/wp-content/uploads/\d{4}/\d{2}/\S+\.pdf$')
        d.extract()

        for a in d.findAll('a', href=r):
            if a.img:
                continue

            g = a.findPrevious('strong')
            job = Job(company=self.company)
            job.title = g.text
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

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return NetsertiveJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
