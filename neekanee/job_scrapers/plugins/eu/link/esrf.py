import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'European Radiation Synchrotron Facility',
    'hq': 'Grenoble, France',

    'home_page_url': 'http://www.esrf.eu',
    'jobs_page_url': 'http://esrf.profilsearch.com/recrute/fo_annonce_lister.php?_lang=en',

    'empcnt': [201,500]
}

class EsrfJobScraper(JobScraper):
    def __init__(self):
        super(EsrfJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^fo_annonce_voir\.php\?id=\d+$')
        
        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
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

            s = soupify(self.br.response().read())
            f = s.find('form', id='MainForm')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return EsrfJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
