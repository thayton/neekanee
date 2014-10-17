import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Faulkner University',
    'hq': 'Montgomery, AL',

    'home_page_url': 'http://www.faulkner.edu',
    'jobs_page_url': 'https://www.prospera.com/CareerHubViewer/CareerHub.aspx?ID=FaulknerUniversity_external_Checksum=PRS358',

    'empcnt': [501,1000]
}

class FaulknerJobScraper(JobScraper):
    def __init__(self):
        super(FaulknerJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^Post\.aspx\?')
        x = {'href': r, 'id': True}

        for a in s.findAll('a', attrs=x):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-2].text)
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

            s = soupify(self.br.response().read())
            d = s.find('div', id='pnlPost')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return FaulknerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
