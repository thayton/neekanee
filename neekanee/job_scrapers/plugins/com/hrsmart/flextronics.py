import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Flextronics',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.flextronics.com',
    'jobs_page_url': 'https://flextronics.hua.hrsmart.com/custom/flex/jobs/',

    'empcnt': [10001]
}

class FlextronicsJobScraper(JobScraper):
    def __init__(self):
        super(FlextronicsJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^\d+\.html$')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='app_main_id')
            v = d.find('div', id='job_details_hua_location_id')

            if not v:
                continue

            l = self.parse_location(v.text)

            if not l:
                continue
            
            job.title = d.h2.text
            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return FlextronicsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
