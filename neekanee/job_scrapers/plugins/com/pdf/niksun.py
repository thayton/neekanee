import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.txtextract.pdftohtml import pdftohtml
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'NIKSUN',
    'hq': 'Princeton, NJ',

    'contact': 'jobs@niksun.com',
    'benefits': {
        'vacation': [(0,18)],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.niksun.com',
    'jobs_page_url': 'http://www.niksun.com/job_openings.php',

    'empcnt': [201,500]
}

class NiksunJobScraper(JobScraper):
    def __init__(self):
        super(NiksunJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^jobsPosting/\w+\.pdf$')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.location = l
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            
            if job.url.find(' ') != -1:
                job.url = urllib.quote(job.url, ':/')

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
    return NiksunJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
