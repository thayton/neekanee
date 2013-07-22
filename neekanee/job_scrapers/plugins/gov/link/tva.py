import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tennessee Valley Authority',
    'hq': 'Knoxville, TN',

    'home_page_url': 'http://www.tva.gov',
    'jobs_page_url': 'https://jobs.tva.com/pljb/tva/external/applicant/index.jsp',

    'empcnt': [10001]
}

class TvaJobScraper(JobScraper):
    def __init__(self):
        super(TvaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text='Search for Jobs'))
        self.br.select_form('searchform')
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            f = s.find('form', attrs={'name': 'joblist'})
            r = re.compile(r'^/pljb/global_jsp/applicant/DisplayJob/JobDetails\.jsp\S+id=\d+$')
        
            for a in f.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[3].text)
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
            x = {'class': 'head2'}
            t = s.find('td', attrs=x)
            t = t.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return TvaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
