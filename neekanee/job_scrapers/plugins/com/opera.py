import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Opera Software',
    'hq': 'San Mateo, CA',

    'home_page_url': 'http://www.opera.com',
    'jobs_page_url': 'http://www.opera.com/company/jobs/list/?dept=all&location=all',

    'empcnt': [501,1000]
}

class OperaJobScraper(JobScraper):
    def __init__(self):
        super(OperaJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/company/jobs/opening/\d+/$')
        d = s.find('div', attrs={'class': 'joblist'})
        d.extract()

        for a in d.findAll('a', href=r):
            v = a.findNext('dd')
            l = v.contents[1].split(';')[0]
            l = self.parse_location(l)

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
            d = s.find('div', attrs={'class': 'article'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return OperaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
