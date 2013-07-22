import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'FedEx',
    'hq': 'Memphis, TN',

    'ats': 'HodesIQ',

    'home_page_url': 'http://www.fedex.com',
    'jobs_page_url': 'http://fedex.hodesiq.com/careers/job_search.aspx?Locale=en',

    'empcnt': [10001]
}

class FedExJobScraper(JobScraper):
    def __init__(self):
        super(FedExJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('frm')
        self.br.form['txtcountry'] = ['US']
        self.br.submit()

        r = re.compile(r'^job_detail\.aspx\?')

        while True:
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
                job.url = urlutil.url_query_del(job.url, 'User_ID')
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            i = s.find('input', id='btnNext')
            if not i:
                break

            self.br.select_form('frm')
            self.br.submit(id='btnNext')

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', id='JobDetail')
            
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return FedExJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
