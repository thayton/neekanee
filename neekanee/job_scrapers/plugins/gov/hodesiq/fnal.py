import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Fermilab',
    'hq': 'Batavia, IL',

    'ats': 'HodesIQ',

    'home_page_url': 'http://www.fnal.gov',
    'jobs_page_url': 'https://fermi.hodesiq.com',

    'empcnt': [1001,5000]
}

class FnalJobScraper(JobScraper):
    def __init__(self):
        super(FnalJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('frm')
        self.br.form.set_all_readonly(False)
        self.br.form['category'] = ''
        self.br.submit('Submit2')

        r = re.compile(r'^job_detail\.asp\?JobID=\d+')

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                if a.parent != td[1]:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

            # Navigate to the next page
            try:
                x = re.compile(r'^Next')
                n = self.br.find_link(text_regex=x)
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
            d = s.find('div', id='right-column-body')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return FnalJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
