import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'The Pew Charitable Trusts',
    'hq': 'Philadelphia, PA',

    'ats': 'icims',

    'home_page_url': 'http://www.pewtrusts.org',
    'jobs_page_url': 'https://jobs-pct.icims.com/jobs/intro',

    'empcnt': [501,1000]
}

class PewTrustsJobScraper(JobScraper):
    def __init__(self):
        super(PewTrustsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('searchForm')
        self.br.submit()

        pageno = 2
        r = re.compile(r'jobs/\d+/\S+/job$')

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[-1].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            try:
                x = re.compile(r'/jobs/search\?pr=' + str(pageno))
                pageno += 1
                self.br.follow_link(self.br.find_link(url_regex=x))
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
            a = {'class': 'iCIMS_MainTable iCIMS_JobPage'}
            t = s.find('table', attrs=a)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return PewTrustsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
