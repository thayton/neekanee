import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Omni Energy',
    'hq': 'Houston, TX',

    'home_page_url': 'http://www.omnienergy.com',
    'jobs_page_url': 'http://www.gibsons.com/Careers/US-Careers.aspx',

    'empcnt': [201,500]
}

class OmniEnergyJobScraper(JobScraper):
    def __init__(self):
        super(OmniEnergyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^^/Careers/US-Careers/Career-U-S\.aspx\?ItemID=\d+$')

        for a in s.findAll('a', href=r):
            d = a.findParent('div')
            p = d.findAll('span')

            l = self.parse_location(p[1].text)
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
            d = s.find('div', id='careerIndv')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return OmniEnergyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
