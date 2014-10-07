import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'USAA',
    'hq': 'San Antonio, TX',

    'home_page_url': 'http://www.usaa.com',
    'jobs_page_url': 'https://search.usaajobs.com/en-US/Search-Jobs/Xsjp',

    'empcnt': [10001]
}
    
class UsaaJobScraper(JobScraper):
    def __init__(self):
        super(UsaaJobScraper, self).__init__(COMPANY)
        
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r"__doPostBack\('([^']+)")
        f = lambda x: x.name == 'a' and x.text == 'Search'
        a = s.find(f)
        m = re.search(r, a['href'])

        def select_form(form):
            return form.attrs.get('id', None) == 'Form1'

        self.br.select_form(predicate=select_form)
        self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': m.group(1)})
        self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
        self.br.form.new_control('hidden', '__LASTFOCUS',     {'value': ''})
        self.br.form.fixup()
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'^/en-US/Job-Details/')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')
            
            l = td[-2].text + ', ' + td[-1].text
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
            d = s.find('div', id='CenterColumn')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return UsaaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
