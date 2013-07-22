import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vishay',
    'hq': 'Malvern, PA',

    'home_page_url': 'http://www.vishay.com',
    'jobs_page_url': 'http://hr.vishay.com',

    'empcnt': [10001]
}

class VishayJobScraper(JobScraper):
    def __init__(self):
        super(VishayJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('webform')
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='jobs')
            r = re.compile(r'^job_details\.aspx\?j=\d+$')
        
            for a in t.findAll('a', href=r):
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

            try:
                self.br.find_link(text='Next')
                self.br.select_form('webform')
                self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': 'Nextbutton'})
                self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
                self.br.form.new_control('hidden', '__LASTFOCUS',     {'value': ''})
                self.br.form.fixup()

                ctl = self.br.form.find_control('btnSearch')
                self.br.form.controls.remove(ctl)

                self.br.submit()
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form', id='webform')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return VishayJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
