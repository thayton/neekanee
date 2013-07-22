import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Major Drilling',
    'hq': 'Moncton, Canada',

    'home_page_url': 'http://www.majordrilling.com',
    'jobs_page_url': 'http://careers2.hiredesk.net/ViewJobs/Default.asp?Comp=MajorDrilling&TP_ID=1',

    'empcnt': [1001,5000]
}

class MajorDrillingJobScraper(JobScraper):
    def __init__(self):
        super(MajorDrillingJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/viewjobs/JobDetail\.asp\?')
        t = s.find('table', id='TPMainTbl')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')
            
            l = self.parse_location(td[1].text + ', ' + td[2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', id='TPMainTbl')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return MajorDrillingJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
