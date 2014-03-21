import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Basis Technology',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.basistech.com',
    'jobs_page_url': 'https://theapplicantmanager.com/jobfeeds/bt.js',
    'jobs_page_daomin': 'theapplicantmanager.com',

    'empcnt': [51,200]
}

class BasisTechJobScraper(JobScraper):
    def __init__(self):
        super(BasisTechJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        d = self.br.response().read()
        r = re.compile(r'"(http://[^?]+\?pos=[A-Z0-9]+)[^>]+>([^<]+)')
        x = re.compile(r'\(([^)]+)')

        for url,title in re.findall(r, d):
            m = re.search(x, title)
            if not m:
                continue

            l = self.parse_location(m.group(1))
            if not l:
                continue

            job = Job(company=self.company)
            job.title = title
            job.url = urlparse.urljoin(self.br.geturl(), url)
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
            d = s.find('div', id='app_content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BasisTechJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

