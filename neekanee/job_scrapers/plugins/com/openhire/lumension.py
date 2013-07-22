import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lumension',
    'hq': 'Seattle, WA',

    'ats': 'OpenHire',

    'home_page_url': 'http://www.lumension.com',
    'jobs_page_url': 'https://lumension.silkroad.com/epostings/index.cfm?company_id=15612',

    'empcnt': [201,500]
}

class LumensionJobScraper(JobScraper):
    def __init__(self):
        super(LumensionJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('frmsearch')
        self.br.form.set_all_readonly(False)
        self.br.form['bycountry'] = '1'
        self.br.form['byLocation'] = ['US']
        self.br.submit()

        r = re.compile(r'index\.cfm\?fuseaction=app\.jobinfo')
        s = soupify(self.br.response().read())

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[2].text)
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
    return LumensionJobScraper()
