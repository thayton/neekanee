import re, urllib, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields
from neekanee.urlutil import url_query_get

from neekanee_solr.models import *

COMPANY = {
    'name': 'DePaul University',
    'hq': 'Chicago, IL',

    'home_page_url': 'http://www.depaul.edu',
    'jobs_page_url': 'https://pshr.depaul.edu/psc/HRPRD92/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_SCHJOB&Action=U&FOCUS=Applicant&SiteId=1',

    'empcnt': [1001,5000]
}

class DePaulJobScraper(JobScraper):
    def __init__(self):
        super(DePaulJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^POSTINGLINK\$\d+$')

        for a in s.findAll('a', id=r):
            # 
            # Click on 'Email to Friend' and you'll see that the permanent
            # link for job postings is as follows
            #
            # https://pshr.depaul.edu/psp/HRPRD92/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=1&JobOpeningId=1664&PostingSeq=1
            #
            b = '/psp/HRPRD92/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL?Page=HRS_APP_JBPST&Action=U&FOCUS=Applicant&SiteId=%d&JobOpeningId=%d&PostingSeq=1'
                    
            x = re.compile(r"javascript:submitAction_win0\(document.win0, '#ICSetFieldHRS_APP_SCHJOB.HRS_JOB_OPEN_ID_PB\.(\d+)'")
            m = re.search(x, a['href'])
            jobid = int(m.group(1))

            siteid = url_query_get(self.br.geturl(), 'SiteId')
            siteid = int(siteid['SiteId'])

            u = b % (siteid, jobid)
            u = urlparse.urljoin(self.br.geturl(), u)

            job = Job(company=self.company)
            job.title = a.text
            job.url = u
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)
            self.br.follow_link(self.br.find_link(tag='iframe', name='TargetContent'))

            s = soupify(self.br.response().read())
            x = { 'name': 'win0' }
            f = s.find('form', attrs=x)

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return DePaulJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
