import re, urllib, urlparse, mechanize, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

COMPANY = {
    'name': 'BB&T',
    'hq': 'Winston-Salem, NC',

    'ats': 'Kenexa',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.bbt.com',
    'jobs_page_url': 'https://recruiter.kenexa.com/bbt/cc/Home.ss?ccid=bupJEdUjsTs%3D',

    'bptw_glassdoor': True,

    'empcnt': [10001]
}

class BbtJobScraper(JobScraper):
    def __init__(self):
        super(BbtJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('form')
        self.br.form.set_all_readonly(False)

        newaction = 'CCJobSearchAction.ss?command=CCSearchPage&ccid=' + self.br.form['ccid']

        self.br.form.action = urlparse.urljoin(self.br.form.action, newaction)
        self.br.submit()

        self.br.select_form('form')
        self.br.form.set_all_readonly(False)

        newaction = 'CCJobSearchAction.ss?command=CCSearchAll'

        self.br.form.action = urlparse.urljoin(self.br.form.action, newaction)
        self.br.submit()

        r = re.compile(r'^javascript:job_JOB_TITLE_ID_onClick\(\'(\d+)\'\)')
        pageno = 2

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                def myesc(x):
                    x = x.replace('&nbsp;', '')
                    x = ' '.join(x.split())
                    return x

                l = myesc(td[-2].text)  + ',' + myesc(td[-1].text)
                l = self.parse_location(l)
                m = re.search(r, a['href'])

                if not l:
                    continue

                f = s.find('form', attrs={'name': 'form'})
                d = extract_form_fields(f)

                #
                # Required query parameters:
                # command=ViewJobDetails&job_REQUISITION_NUMBER=276969&ccid=bupJEdUjsTs%3D&
                #
                newaction = 'CCJobResultsAction.ss?command=ViewJobDetails&job_REQUISITION_NUMBER=' + m.group(1)
                newaction += '&' + urllib.urlencode({'ccid': d['ccid']})

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), newaction)
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            try:
                # Look for link just to trigger LinkNotFoundError
                p = r'javascript:navPage\(\'' + str(pageno) + '\'\)'
                n = self.br.find_link(url_regex=p) 

                self.br.select_form('form')
                self.br.form.set_all_readonly(False)

                newaction = 'CCJobResultsAction.ss?command=MoveToPage'

                self.br.form.action = urlparse.urljoin(self.br.form.action, newaction)
                self.br.form['PageNumber'] = str(pageno)
                self.br.submit()

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

            x = soupify(self.br.response().read())
            g = x.find('form', attrs={'name': 'form'})

            job.desc = get_all_text(g)
            job.save()
            
def get_scraper():
    return BbtJobScraper()
