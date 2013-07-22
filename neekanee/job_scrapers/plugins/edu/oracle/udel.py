import re, urllib, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields
from neekanee.urlutil import url_query_get

from neekanee_solr.models import *

COMPANY = {
    'name': 'University of Delaware',
    'hq': 'Newark, DE',

    'home_page_url': 'http://www.udel.edu',
    'jobs_page_url': 'http://www.udel.edu/udjobs/',

    'empcnt': [1001,5000]
}

class UdelJobScraper(JobScraper):
    def __init__(self):
        super(UdelJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        link_text_list = [ 'Faculty', 'Staff', 'Maintenance | Service' ]

        for link_text in link_text_list:
            def select_iframe(iframe):
                return dict(iframe.attrs).get('id', None) == 'main'

            self.br.open(url)
            self.br.follow_link(self.br.find_link(text=link_text))
            self.br.follow_link(self.br.find_link(tag='iframe', predicate=select_iframe))

            b = '/psp/RESUME/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_CE.GBL?Page=HRS_CE_JOB_DTL&Action=A&JobOpeningId=%d&SiteId=%d&PostingSeq=1'
            r = re.compile(r'^POSTINGTITLE\$\d+$')

            siteid = url_query_get(self.br.geturl(), 'SiteId')
            siteid = int(siteid['SiteId'])

            while True:
                s = soupify(self.br.response().read())

                for a in s.findAll('a', id=r):
                    tr = a.findParent('tr')
                    td = tr.findAll('td')

                    l = td[-1].text.strip()
                    
                    if len(l) == 0:
                        continue

                    l = l.lower()
                    if l == 'newark':
                        l = 'newark, de'

                    l = self.parse_location(l)
                    if not l:
                        continue

                    jobid = int(td[-2].text)
                    
                    u = b % (jobid, siteid)
                    u = urlparse.urljoin(self.br.geturl(), u)

                    job = Job(company=self.company)
                    job.title = a.text
                    job.url = u
                    job.location = self.company.location
                    jobs.append(job)

                a = s.find('a', id='HRS_APPL_WRK_HRS_LST_NEXT')
                if not a:
                    break

                self.br.select_form('win0')
                self.br.set_all_readonly(False)
                self.br.form['ICAction'] = 'HRS_APPL_WRK_HRS_LST_NEXT'
                self.br.submit()

            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)
            self.br.follow_link(self.br.find_link(tag='iframe', name='TargetContent'))

            s = soupify(self.br.response().read())
            x = {'id': 'ACE_width', 'class': 'PSPAGECONTAINER'}
            t = s.find('table', attrs=x)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return UdelJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
