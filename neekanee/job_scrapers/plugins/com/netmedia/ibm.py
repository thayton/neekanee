import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'IBM',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.ibm.com',
    'jobs_page_url': 'https://jobs3.netmedia1.com/cp/faces/job_search',

    'empcnt': [10001]
}

class IbmJobScraper(JobScraper):
    def __init__(self):
        super(IbmJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('myForm')
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='myForm:job-table')
            r = re.compile(r'job_summary\?job_id=[\w-]+$')

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = ' '.join(['%s' % getattr(x, 'text', x) for x in td[2].contents])
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Next >'))
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
            x = {'class': 'job-summary-page'}
            t = s.find('table', attrs=x)

            if not t:
                continue

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return IbmJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
