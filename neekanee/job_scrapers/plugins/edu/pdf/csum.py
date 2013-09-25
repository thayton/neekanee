import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'California Maritime Academy',
    'hq': 'Vallejo, CA',

    'home_page_url': 'http://www.csum.edu',
    'jobs_page_url': 'http://www.csum.edu/web/hr/careers',

    'empcnt': [201,500]
}

class CsumJobScraper(JobScraper):
    def __init__(self):
        super(CsumJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        link_text = ['Faculty', 'Management', 'Staff']
        
        for t in link_text:
            self.br.follow_link(self.br.find_link(text=t))

            s = soupify(self.br.response().read())
            r = re.compile(r'get_file\?uuid=[a-z0-9-]+')

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                job = Job(company=self.company)
                job.title = td[1].text
                job.url = urlparse.urljoin(self.br.geturl(), td[0].a['href'])
                job.location = self.company.location
                jobs.append(job)
                break

            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            d = self.br.response().read()
            s = soupify(pdftohtml(data))

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CsumJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
