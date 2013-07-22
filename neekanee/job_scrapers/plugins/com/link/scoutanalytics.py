import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ScoutAnalytics',
    'hq': 'Issaquah, WA',

    'home_page_url': 'http://scoutanalytics.com',
    'jobs_page_url': 'http://www.scoutanalytics.com/careers.php',

    'empcnt': [11,50]
}

class ScoutAnalyticsJobScraper(JobScraper):
    def __init__(self):
        super(ScoutAnalyticsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^careers_full\.php\?pdx=\d+$')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
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
            x = {'class': 'contentMainFull'}
            d = s.find('div', attrs=x)

            y = {'class': 'doBold'}
            r = re.compile(r'location:\s*', re.I)
            l = s.find('p', attrs=y)
            l = re.sub(r, '', l.text)
            l = self.parse_location(l)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ScoutAnalyticsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
