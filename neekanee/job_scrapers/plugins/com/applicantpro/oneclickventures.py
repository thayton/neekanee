import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'One Click Ventures',
    'hq': 'Greenwood, IN',

    'home_page_url': 'http://www.oneclickventures.com',
    'jobs_page_url': 'http://oneclickventures.applicantpro.com/jobs/',

    'empcnt': [11,50]
}

class OneClickVenturesJobScraper(JobScraper):
    def __init__(self):
        super(OneClickVenturesJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', id='job_listing')
        r = re.compile(r'^/jobs/\d+\.html$')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[1].text)
            if l is None:
                l = self.company.location

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
            d = s.find('div', attrs={'class': 'panel'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return OneClickVenturesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
