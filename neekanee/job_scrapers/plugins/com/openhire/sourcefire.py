import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Sourcefire',
    'hq': 'Columbia, MD',

    'ats': 'OpenHire',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.sourcefire.com',
    'jobs_page_url': 'https://sourcefire.silkroad.com/epostings/',

    'empcnt': [201,500]
}

class SourcefireJobScraper(JobScraper):
    def __init__(self):
        super(SourcefireJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('frmsearch')
        self.br.form.set_all_readonly(False)
        self.br.form['bycountry'] = '1'
        self.br.form['byLocation'] = ['US.']
        self.br.submit()

        s = soupify(self.br.response().read())
        for a in s.findAll('a', href=re.compile(r'index.cfm\?fuseaction=app\.jobinfo')):
            l = a.findParent('td').findNext('td').string

            if l.find(', US') == -1:
                continue

            l = re.sub(r',\s+US', '', l)
            l = self.parse_location(l)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.location = l
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
            d = s.find('div', id='content-inner')
            d = d.findAll('div', id=re.compile(r'\w+'))
            job.desc = ' '

            for t in d:
                job.desc += ' ' + get_all_text(t)

            job.save()

def get_scraper():
    return SourcefireJobScraper()


