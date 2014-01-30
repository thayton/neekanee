import re, urlparse, json, mechanize, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, repair

from neekanee_solr.models import *

COMPANY = {
    'name': 'Marriott International',
    'hq': 'Bethesda, MD',

    'home_page_url': 'http://www.marriott.com',
    'jobs_page_url': 'http://jobs.marriott.com/careers/SearchJobsData?lang=en',

    'empcnt': [10001]
}

class MarriottJobScraper(JobScraper):
    def __init__(self):
        super(MarriottJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        offset = 0
        data_orig = {'offset': '%d'}

        while True:
            data = data_orig.copy()
            data['offset'] = data['offset'] % offset

            data = urllib.urlencode(data)
            resp = mechanize.Request(url, data)
            
            r = mechanize.urlopen(resp)
            d = json.loads(repair(r.read()))
            v = d['jobs'].values()

            if len(v) == 0:
                break

            for j in v:
                l = self.parse_location(j['location'])
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = j['title']
                job.url = j['url']
                job.location = l
                jobs.append(job)

            offset += 10

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='jobData')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MarriottJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
