import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Sabre Hospitality Solutions',
    'hq': 'Southlake, TX',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.sabrehospitality.com',
    'jobs_page_url': 'http://www.sabrehospitality.com/hospitality-careers.php',

    'empcnt': [201,500]
}

class SabreHospitalityJobScraper(JobScraper):
    def __init__(self):
        super(SabreHospitalityJobScraper, self).__init__(COMPANY)
        
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/hospitality-careers-listing.php\?id=[0-9]+')

        for a in s.findAll('a', href=r):
            d = {'class': 'location'}
            l = a.findNext('span', attrs=d)
            if l is None:
                continue

            x = self.parse_location(l.text)
            if x is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = x
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.html.h1.parent

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SabreHospitalityJobScraper()
