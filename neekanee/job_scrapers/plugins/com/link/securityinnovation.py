import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Security Innovation',
    'hq': 'Wilmington, MA',

    'home_page_url': 'http://securityinnovation.com',
    'jobs_page_url': 'https://www.securityinnovation.com/company/about-us/careers/',

    'empcnt': [51,200]
}

class SecurityInnovationJobScraper(JobScraper):
    def __init__(self):
        super(SecurityInnovationJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        d.extract()

        locations = {'boston': self.parse_location('boston, ma'),
                     'seattle': self.parse_location('seattle, wa')}

        r = re.compile(r'^company/about-us/careers/\S+\.html$')

        for a in d.findAll('a', href=r):
            h = a.findPrevious('h2')
            l = locations[h.text.lower()]

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.company.home_page_url, a['href'])
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
            d = s.find('div', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SecurityInnovationJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
