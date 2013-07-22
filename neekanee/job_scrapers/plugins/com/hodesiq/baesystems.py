import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BAE Systems',
    'hq': 'London, UK',

    'ats': 'HodesIQ',

    'home_page_url': 'http://www.baesystems.com',
    'jobs_page_url': 'http://baesystems.hodesiq.com/job_start.asp',

    'empcnt': [10001]
}

class BaeSystemsJobScraper(JobScraper):
    def __init__(self):
        super(BaeSystemsJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('frm')
        self.br.form.action = urlparse.urljoin(self.br.geturl(), 'joblist.asp')
        self.br.submit()

        r = re.compile(r'javascript:SubmitForm\((\d+)\)')

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                if a.parent != td[1]:
                    continue

                l = self.parse_location(td[-1].text)
                if not l:
                    continue

                m = re.search(r, a['href'])
                if not m:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), 'job_detail.asp?JobID=' + m.group(1))
                job.location = l
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
            d = s.find('div', id='iq-page-content-container')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BaeSystemsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
