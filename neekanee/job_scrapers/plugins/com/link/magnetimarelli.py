import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Magneti Marelli',
    'hq': 'Corbetta, Italy',

    'home_page_url': 'http://www.magnetimarelli.com',
    'jobs_page_url': 'http://www.magnetimarelli.com/sites/all/careers_files/en/index.html',

    'empcnt': [10001]
}

class MagnetiMarelliJobScraper(JobScraper):
    def __init__(self):
        super(MagnetiMarelliJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'title': 'Job Search'}
        a = s.find('a', attrs=x)

        self.br.open(a['href'])
        self.br.select_form(nr=0)
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='TableJobs')
            r = re.compile(r'nPostingID=\d+')
        
            for a in d.findAll('a', href=r):
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

            try:
                r = re.compile(r'pagenum=%d' % pageno)
                self.br.follow_link(self.br.find_link(url_regex=r))
                pageno += 1
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
            d = s.find('div', id='JDescContent')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MagnetiMarelliJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
