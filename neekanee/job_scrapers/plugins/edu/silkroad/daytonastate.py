import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Daytona State College',
    'hq': 'Daytona Beach, FL',

    'home_page_url': 'http://www.daytonastate.edu',
    'jobs_page_url': 'https://daytonastate-openhire.silkroad.com/epostings/',

    'empcnt': [1001,5000]
}

class DaytonaStateJobScraper(JobScraper):
    def __init__(self):
        super(DaytonaStateJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'frmsearch'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit('Search')

        s = soupify(self.br.response().read())
        r = re.compile(r'^index\.cfm\?fuseaction=app\.jobinfo')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-2].text)
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

        for job in job_list:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form', id='applyJob')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return DaytonaStateJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
