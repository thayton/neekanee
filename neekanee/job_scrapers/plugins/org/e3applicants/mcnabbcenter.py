import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Helen Ross McNabb Center',
    'hq': 'Knoxville, TN',

    'home_page_url': 'http://www.mcnabbcenter.org',
    'jobs_page_url': 'https://www.e3applicants.com/hrm/CareersFrame.aspx',

    'empcnt': [201,500]
}

class McnabbCenterJobScraper(JobScraper):
    def __init__(self):
        super(McnabbCenterJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            f = s.find('form', id='aspnetForm')
            x = {'class': 'job-title'}
            r = re.compile(r'"(posting\.aspx[^"]+)')

            for d in f.findAll('div', attrs=x):
                m = re.search(r, d.a['onclick'])
                u = urlparse.urljoin(self.br.geturl(), m.group(1))

                job = Job(company=self.company)
                job.title = d.a.text
                job.url = u
                job.location = self.company.location
                jobs.append(job)
                break
                
            self.br.select_form('aspnetForm')
            self.br.subit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return McnabbCenterJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
