import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tennessee Valley Authority',
    'hq': 'Knoxville, TN',

    'home_page_url': 'http://www.tva.gov',
    'jobs_page_url': 'https://careers.tva.gov/psc/hcmpcg/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_CE.GBL',

    'empcnt': [10001]
}

class TvaJobScraper(JobScraper):
    def __init__(self):
        super(TvaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^POSTINGTITLE\$\d+$')
            x = {'id': r, 'name': r}

            for a in s.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[-1].text)
                if not l:
                    continue

                # 
                # If you click on "Email to Friend" you'll see that
                # this is the link that is used to refer to a specific
                # posting
                #
                # https://careers.tva.gov/psp/hcmpcg/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_CE.GBL?Page=HRS_CE_JOB_DTL&Action=A&JobOpeningId=500193&SiteId=1&PostingSeq=1
                # https://exelonjobs.ceco.com/psc/HRPC_TAM/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_CE.GBL?Page=HRS_CE_JOB_DTL&Action=A&JobOpeningId=3006838&SiteId=1&PostingSeq=1
                #
                jobid = td[-2].text

                url = 'https://careers.tva.gov/psp/hcmpcg/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_CE.GBL?Page=HRS_CE_JOB_DTL&Action=A&JobOpeningId=%s&SiteId=1&PostingSeq=1'
                url = url % jobid

                job = Job(company=self.company)
                job.title = a.text
                job.location = l
                job.url = url
                jobs.append(job)

            a = s.find('a', id='HRS_APPL_WRK_HRS_LST_NEXT')
            if not a:
                break

            self.br.select_form('win0')
            self.br.set_all_readonly(False)
            self.br.form['ICAction'] = 'HRS_APPL_WRK_HRS_LST_NEXT'
            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)
            self.br.follow_link(self.br.find_link(tag='iframe', name='TargetContent'))

            z = soupify(self.br.response().read())
            d = z.find('div', id='win0divPSPAGECONTAINER')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TvaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
