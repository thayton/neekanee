import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lahey Clinic',
    'hq': 'Burlington, MA',

    'home_page_url': 'http://www.lahey.org/',
    'jobs_page_url': 'https://jobs.lahey.org/psp/erecruit/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_CE.GBL?NAVSTACK=Clear',

    'empcnt': [5001,10000]
}

class LaheyJobScraper(JobScraper):
    def __init__(self):
        super(LaheyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(tag='frame', name='TargetContent'))

        b = '/psp/erecruit/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_CE.GBL?Page=HRS_CE_JOB_DTL&Action=A&JobOpeningId=%d&SiteId=1&PostingSeq=1'
        r = re.compile(r'^POSTINGTITLE\$\d+$')
        x = {'id': r, 'class': 'PSHYPERLINK'}

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[-1].text.strip()
                if l.lower() == 'burlington':
                    l += ', ma'

                l = self.parse_location(l)
                if not l:
                    continue

                jobid = int(td[-2].text)

                u = b % jobid
                u = urlparse.urljoin(self.br.geturl(), u)

                job = Job(company=self.company)
                job.title = a.text
                job.url = u
                job.location = l
                jobs.append(job)
                break

            a = s.find('a', id='HRS_APPL_WRK_HRS_LST_NEXT')
            if not a:
                break

            self.br.select_form('win0')
            self.br.set_all_readonly(False)
            self.br.form['ICAction'] = 'HRS_APPL_WRK_HRS_LST_NEXT'
            self.br.submit()
            break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)
            self.br.follow_link(self.br.find_link(tag='frame', name='TargetContent'))

            s = soupify(self.br.response().read())
            x = {'id': 'ACE_width', 'class': 'PSPAGECONTAINER'}
            t = s.find('table', attrs=x)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return LaheyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
