import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Radio Flyer',
    'hq': 'Chicago, IL',

    'ats': 'OpenHire',

    'home_page_url': 'http://www.radioflyer.com',
    'jobs_page_url': 'https://hostedjobs.openhire.com/epostings/submit.cfm?fuseaction=app.allpositions&company_id=16014&version=1',

    'empcnt': [51,200]
}

class RadioFlyerJobScraper(JobScraper):
    def __init__(self):
        super(RadioFlyerJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'cssAllJobListBody'})
        r = re.compile(r'/epostings/submit\.cfm\?fuseaction=app.jobinfo&jobid=\d+')

        for a in d.findAll('a', href=r):
            v = a.findParent('div')
            l = self.parse_location(v.contents[-1])
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
            f = s.find('form', id='applyJob')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return RadioFlyerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
