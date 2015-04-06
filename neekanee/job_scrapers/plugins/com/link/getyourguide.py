import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'GetYourGuide',
    'hq': 'Zurich, Switzerland',

    'home_page_url': 'http://www.getyourguide.com',
    'jobs_page_url': 'http://careers.getyourguide.com/all-jobs',

    'empcnt': [201,500]
}

class GetYourGuideJobScraper(JobScraper):
    def __init__(self):
        super(GetYourGuideJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/\?gh_jid=\d+$')

        for a in s.findAll('a', href=r):
            h3 = a.findPrevious('h3')
            l = self.parse_location(h3.text)
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
            r = re.compile(r'\bjob_offer_info\b')
            x = {'class': r}
            n = s.find('section', attrs=x)
            x = {'class': 'container'}
            d = n.findParent('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return GetYourGuideJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
