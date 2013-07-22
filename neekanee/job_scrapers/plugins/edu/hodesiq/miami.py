import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Universiy of Miami',
    'hq': 'Miami, FL',

    'ats': 'HodesIQ',
    'benefits': {
        'url': 'http://www.miami.edu/index.php/benefits_administration/',
        'vacation': [(1,10),(3,15),(11,22)],
        'holidays': 13
    },

    'home_page_url': 'http://www.miami.edu',
    'jobs_page_url': 'http://um.hodesiq.com/job_start.asp',

    'empcnt': [5001,10000]
}

class MiamiJobScraper(JobScraper):
    def __init__(self):
        super(MiamiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('frm')
        self.br.submit()

        r = re.compile(r'^job_detail\.asp\?JobID=[0-9]+')

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'main-col-wide'})
            t = d.table

            for a in t.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = urlutil.url_query_del(job.url, ['user_id', 'ViewAll'])
                job.location = self.company.location
                jobs.append(job)

            # Navigate to the next page
            try:
                n = self.br.find_link(text='Next')
            except mechanize.LinkNotFoundError:
                break

            self.br.select_form('frm')

            x = self.br.form.find_control('move_indicator')
            x.readonly = False

            self.br.form['move_indicator'] = 'next'
            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', id='Table1')
            t = t.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return MiamiJobScraper()
