import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Kodiak Oil & Gas',
    'hq': 'Denver, CO',

    'home_page_url': 'http://www.kodiakog.com',
    'jobs_page_url': 'http://www.kodiakog.com/careers/careers.html',

    'empcnt': [11,50],
}

class KodiakJobScraper(JobScraper):
    def __init__(self):
        super(KodiakJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        locations = { 'denver.html': self.parse_location('Denver, CO'),
                      'northdakota.html': self.parse_location('Dickinson, ND') }


        for k,v in locations.items():
            try:
                self.br.follow_link(self.br.find_link(url=k))
            except:
                continue

            s = soupify(self.br.response().read())
            r = re.compile(r'/pdf/\S+\.pdf$')    

            for a in s.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = v
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
    return KodiakJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
