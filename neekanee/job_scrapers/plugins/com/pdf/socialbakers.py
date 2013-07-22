import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'SocialBakers',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.socialbakers.com',
    'jobs_page_url': 'http://www.socialbakers.com/careers',

    'empcnt': [201,500],
}

class SocialBakersJobScraper(JobScraper):
    def __init__(self):
        super(SocialBakersJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/storage/www/\S+-\d+\.pdf$')
        y = re.compile(r'location', re.I)
        z = re.compile(r'\(([^)]+)')

        for a in s.findAll('a', href=r):
            m = re.search(z, a.text)
            l = re.sub(y, '', m.group(1))
            l = self.parse_location(l)

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

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return SocialBakersJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
