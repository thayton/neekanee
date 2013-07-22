import re, urlparse, urllib, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto, extract_form_fields

from neekanee_solr.models import *

COMPANY = {
    'name': 'Brocade',
    'hq': 'San Jose, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.brocade.com',
    'jobs_page_url': 'http://careers.brocade.com/joblist.asp',

    'empcnt': [1001,5000]
}

class BrocadeJobScraper(JobScraper):
    def __init__(self):
        super(BrocadeJobScraper, self).__init__(COMPANY)
        
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r"javascript:ViewJobDetail\('(\d+)'\)")
        b = {'class': 'SearchResultsTable'}

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', attrs=b)

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')
            
                l = self.parse_location(td[-1].text)
                if l is None:
                    continue

                self.br.select_form('frm')
                self.br.set_all_readonly(False)

                m = re.search(r, a['href'])

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), 'job_detail.asp')
                job.url += '?' + 'JobID=%s' % m.group(1)
                job.location = l
                jobs.append(job)

            # Nagivate to the next page
            try:
                self.br.find_link(text='%s' % pageno)
            except mechanize.LinkNotFoundError:
                break

            self.br.select_form('frm')
            self.br.set_all_readonly(False)
            self.br.form['page'] = '%s' % pageno
            self.br.submit()
            pageno += 1

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            g = soupify(self.br.response().read())
            td = g.find('td', attrs={'class': 'title'})
            td = td.findParent('td')

            job.desc = get_all_text(td)
            job.save()

def get_scraper():
    return BrocadeJobScraper()
