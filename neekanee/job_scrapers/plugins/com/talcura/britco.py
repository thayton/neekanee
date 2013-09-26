import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from BeautifulSoup import BeautifulSoup

from neekanee_solr.models import *

COMPANY = {
    'name': 'Britco',
    'hq': 'Langley, Canada',

    'home_page_url': 'http://www.britco.com',
    'jobs_page_url': 'https://britco.talcura.com/candidates/Default.aspx?&DeptID=0&lang=en',

    'empcnt': [1001,5000]
}

class BritcoJobScraper(JobScraper):
    def __init__(self):
        super(BritcoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'aspnetForm'

        self.br.open(url)

        pageno = 2

        while True:
            s = BeautifulSoup(self.br.response().read())
            r = re.compile(r'^/Candidates/ShowJob\.aspx\?JobId=\d+$')

            for a in s.findAll('a', href=r):
                l = a.h3.contents[-1]
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.h3.span.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            f = lambda x: x.name == 'a' and x.text == '%d' % pageno
            a = s.find(f)

            if not a:
                break

            pageno += 1

            r = re.compile(r"__doPostBack\('([^']+)")
            m = re.search(r, a['href'])

            y = re.compile(r'_TSM_CombinedScripts_=([^"]+)')
            x = {'src': y}
            z = s.find('script', attrs=x)
            x = re.search(y, z['src'])

            self.br.select_form(predicate=select_form)                

            ctl = self.br.form.find_control('ctl00$cphMain$btnSearch')
            self.br.form.controls.remove(ctl)

            ctl = self.br.form.find_control('ctl00$cphMain$dpJobsPager$ctl00$PrevButton')
            self.br.form.controls.remove(ctl)

            ctl = self.br.form.find_control('ctl00$cphMain$dpJobsPager$ctl02$LastButton')
            self.br.form.controls.remove(ctl)

            ctl = self.br.form.find_control('ctl00$cphMain$ucSignIn$btnRegister')
            self.br.form.controls.remove(ctl)
            
            ctl = self.br.form.find_control('ctl00$cphMain$dpJobsPager$ctl02$NextButton')
            self.br.form.controls.remove(ctl)

            ctl = self.br.form.find_control('ctl00$cphMain$ucSignIn$btnSocialSignIn')
            self.br.form.controls.remove(ctl)

            ctl = self.br.form.find_control('ctl00$cphMain$ucSignIn$btnSignIn')
            self.br.form.controls.remove(ctl)

            ctl = self.br.form.find_control('ctl00$cphMain$ucSignIn$btnRecover')
            self.br.form.controls.remove(ctl)

            for n in range(0,5):
                ctl = self.br.form.find_control('ctl00$cphMain$cblJobTypes$%d' % n)
                self.br.form.controls.remove(ctl)
            
            for ctl in self.br.form.controls:
                if re.search(r'Button', ctl.name):
                    self.br.form.controls.remove(ctl)                    

            self.br.form.set_all_readonly(False)
            self.br.form['ctl00_ctl05_TSM'] = urllib.unquote(x.group(1))
            self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': m.group(1)})
            self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
            self.br.form.fixup()
            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'c-j-desc'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BritcoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
