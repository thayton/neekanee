import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Cooper Power Systems',
    'hq': 'Waukesha, WI',

    'benefits': {
        'vacation': [],
        'tuition_assistance': True
     },

    'home_page_url': 'http://www.cooperpower.com',
    'jobs_page_url': 'https://cooperindustries.mua.hrdepartment.com/hrdepartment/ats/JobSearch/viewAll',

    'empcnt': [10001]
}

class CooperPowerJobScraper(JobScraper):
    def __init__(self):
        super(CooperPowerJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        r = re.compile(r'^/hrdepartment/ats/Posting/view/\d+$')
        pageno = 2

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
 
            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[1].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)
                break

            # Navigate to the next page
            try:
                x = re.compile(r'/ats/JobSearch/viewAll/jobSearchPagination_page:%d' % pageno)
                self.br.follow_link(self.br.find_link(url_regex=x))
                pageno += 1
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        self.company.ats = 'Online form'
        
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='hua_main_page')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CooperPowerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
