import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'National University of Singapore',
    'hq': 'Singapore, Singapore',

    'home_page_url': 'http://www.nus.edu.sg',
    'jobs_page_url': 'https://jobs.nus.edu.sg/career/default.asp?AC=OHR&EC=OHR&GC=G01&PID=1',

    'empcnt': [5001,10000]
}

class NusJobScraper(JobScraper):
    def __init__(self):
        super(NusJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r'^Default\.asp\?')

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            f = s.find('form', attrs={'name': 'frmJobList'})
        
            for a in f.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

            i = f.find('input', id='RecNo')
            x = re.compile(r'(\d+)')
            m = re.search(x, i.parent.text)
            n = int(m.group(1))

            if i['value'] == n:
                break

            self.br.select_form('frmJobList')
            self.br.form.set_all_readonly(False)
            self.br.form['GoPage'] = '%d' % pageno
            self.br.form['IsSort'] = 'false'
            self.br.submit()

            pageno += 1

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form', attrs={'name': 'frmJobDetail'})

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return NusJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
