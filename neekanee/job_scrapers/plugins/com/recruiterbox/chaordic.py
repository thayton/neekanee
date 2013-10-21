import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Chaordic',
    'hq': 'Florianopolis, Brazil',

    'home_page_url': 'http://www.chaordic.com.br',
    'jobs_page_url': 'http://chaordic.recruiterbox.com/widget/jobs',

    'empcnt': [51,200]
}

class ChaordicJobScraper(JobScraper):
    def __init__(self):
        super(ChaordicJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/widget/jobs/\d+\?')
        
        for a in s.findAll('a', href=r):
            p = a.findAll('span')
            l = self.parse_location(p[-1].text)
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
            d = s.find('div', id='recruiterbox_job_holder')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ChaordicJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
