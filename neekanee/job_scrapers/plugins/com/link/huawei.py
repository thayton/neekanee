import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Huawei',
    'hq': 'Shenzhen, China',

    'home_page_url': 'http://www.huawei.com',
    'jobs_page_url': 'http://career.huawei.com/career/en/i18n/jobSearch.do?callMethod=doPreSearch',

    'empcnt': [10001]
}

class HuaweiJobScraper(JobScraper):
    def __init__(self):
        super(HuaweiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('queryJobForm')
        self.br.form['resultsPerpage'] = [ '50' ]
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            f = s.find('form', attrs={'name': 'queryJobForm'})
            r = re.compile(r'^/career/en/i18n/toJobDetail\.do\?callMethod=toJobDetail&jobID=\d+$')

            for a in f.findAll('a', href=r):
                tb = a.findParent('table')
                tr = tb.findAll('tr')
                td = tr[1].findAll('td')

                l =  td[-1].text.strip()
                if len(l) == 0:
                    continue

                l = self.parse_location(td[-1].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)
                break

            try:
                self.br.follow_link(self.br.find_link(text='Next'))
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
            d = s.find('div', text='Job Detail')
            t = d.findParent('td')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return HuaweiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
