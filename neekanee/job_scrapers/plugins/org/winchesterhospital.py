import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Winchester Hospital', 
    'hq': 'Winchester, MA',

    'home_page_url': 'http://www.winchesterhospital.org',
    'jobs_page_url': 'http://www.healthcaresource.com/wh/index.cfm?fuseaction=search.categoryList&template=dsp_job_categories.cfm',

    'empcnt': [1001,5000]
}

class WinchesterHospitalJobScraper(JobScraper):
    def __init__(self):
        super(WinchesterHospitalJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            try:
                return form['fuseaction'] == 'search.jobList'
            except:
                return False

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        pageno = 2

        r = re.compile(r'index.cfm\?fuseaction=\S+cJobId=\d+')

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[-1].text + ', MA'
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = a['href']
                job.location = l
                jobs.append(job)

            x = {'value': 'Next Page >>'}
            i = s.find('input', attrs=x)

            if not i:
                break

            try:
                self.br.select_form(name='form')
                self.br.set_all_readonly(False)

                self.br['fuseaction'] = 'search.jobList'
                self.br['template'] = 'dsp_job_list.cfm'
                self.br['iJobCatId'] = '100'
                self.br['iFacilityId'] = '10000'
                self.br['cJobAttr1'] = 'All'
                self.br['iJobRowSet'] = str(pageno)

                pageno += 1
                self.br.submit()
            except:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('td', attrs={'class': 'headline'})
            t = t.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return WinchesterHospitalJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
