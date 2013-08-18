import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Massachusetts Institute of Technology',
    'hq': 'Cambridge, MA',

    'ats': 'Webhire',

    'home_page_url': 'http://www.mit.edu',
    'jobs_page_url': 'http://hrweb.mit.edu/staffing/',

    'empcnt': [5001,10000]
}

class MitJobScraper(JobScraper):
    def __init__(self):
        super(MitJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('search')
        self.br.submit()

        r = re.compile(r'^/servlet/av/jd\?')
        
        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[4].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            try:
                self.br.select_form('GetNextPage')
                self.br.submit()
            except mechanize.FormNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content')

            job.desc = get_all_text(d)    
            job.save()

def get_scraper():
    return MitJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
