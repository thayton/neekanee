import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'MGH Institute of Health Professions',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.mghihp.edu',
    'jobs_page_url': 'http://www.mghihp.edu/about-us/working-at-the-institute/default.aspx',

    'empcnt': [51,200]
}

class MghIhpJobScraper(JobScraper):
    def __init__(self):
        super(MghIhpJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        
        s = soupify(self.br.response().read())
        r = re.compile(r'/about-us/working-at-the-institute/.*-opportunities\.aspx$')

        for l in s.findAll('a', href=r):
            u = urlparse.urljoin(self.br.geturl(), l['href'])

            self.br.open(u)

            x = soupify(self.br.response().read())
            e = re.compile(r'/files/about-us/job-openings/.*\.pdf$')

            for a in x.findAll('a', href=e):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), urllib.quote(a['href'], safe='/:'))
                job.location = self.company.location
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            try:
                self.br.open(job.url)
            except:
                continue

            data = self.br.response().read()
            page = pdftohtml(data)
            html = page.read()

            if html == '':
                return False

            s = soupify(html)

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return MghIhpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
