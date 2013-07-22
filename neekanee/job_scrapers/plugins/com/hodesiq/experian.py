import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Experian',
    'hq': 'Costa Mesa, CA',

    'ats': 'HodesIQ',

    'home_page_url': 'http://www.experian.com',
    'jobs_page_url': 'http://experian.hodesiq.com/index.asp',

    'empcnt': [5001,10000]
}

class ExperianJobScraper(JobScraper):
    def __init__(self):
        super(ExperianJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('searchForm')
        self.br.submit()

        r = re.compile(r'job_detail\.asp\?JobID=[0-9]+')

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[-2].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl() + '/', a['href'])
                job.url = urlutil.url_query_del(job.url, ['user_id', 'ViewAll'])
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
            d = s.find('div', id='mainLeftContent680')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ExperianJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
