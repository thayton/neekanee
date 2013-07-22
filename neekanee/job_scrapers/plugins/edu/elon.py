import re, urllib, urllib2, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from unescape import unescape
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Elon University',
    'hq': 'Elon, NC',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.elon.edu',
    'jobs_page_url': 'https://www.elon.edu/webservices_1/employment/openings.aspx',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

class ElonJobScraper(JobScraper):
    def __init__(self):
        super(ElonJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^javascript:__doPostBack\(\'(.*?)\'')

        for a in s.findAll('a', href=r):
            if not a.text == 'View Description':
                continue

            tr = a.findParent('tr')
            td = tr.findAll('td')

            #
            # These controls are in the form but don't get picked
            # up by mechanize for some reason. So instead we add
            # them manually.
            #
            self.br.select_form('aspnetForm')
            try:
                self.br.form.find_control('__EVENTTARGET')
            except:
                self.br.form.new_control('hidden', '__EVENTTARGET',   {'value':''})
                self.br.form.fixup()

            try:
                self.br.form.find_control('__EVENTARGUMENT')
            except:
                self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value':''})
                self.br.form.fixup()

            self.br.form.set_all_readonly(False)

            m = re.search(r, a['href'])
            self.br.form['__EVENTTARGET'] = m.group(1)
            self.br.form['__EVENTARGUMENT'] = ''

            job = Job(company=self.company)
            job.title = td[0].text
            job.location = self.company.location
            job.url = self.br.geturl()

            form_fields = {}
            for x in self.br.form.controls:
                form_fields[x.name] = x.value

            job.url_data = urllib.urlencode(form_fields)
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            html = self.urlencoded_form_to_html_form(job.url, job.url_data)
            resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                           job.url, 200, "OK")

            self.br.set_response(resp)
            self.br.select_form(nr=0)
            self.br.submit()

            x = soupify(self.br.response().read())
            d = x.find('div', attrs={'class': 'BasicPagePadding'})

            job.desc =  get_all_text(d)
            job.save()

def get_scraper():
    return ElonJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
