import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ledcor',
    'hq': 'Vancouver, Canada',

    'home_page_url': 'http://www.ledcor.com',
    'jobs_page_url': 'http://jobs.ledcor.com/findjob.aspx',

    'empcnt': [10001]
}

class LedcorJobScraper(JobScraper):
    def __init__(self):
        super(LedcorJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r'^jobs/\d+-')
        x = {'class': 'content_list-jobs'}
        y = {'class': 'list-state-city'}

        pageno = 2

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                d = a.findParent('div', attrs=x)
                d = d.find('div', attrs=y)

                l = self.parse_location(d.text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            def select_form(form):
                return form.attrs.get('id', None) == 'aspnetForm'

            f = lambda x: x.name == 'a' and x.text == '%d' % pageno
            a = s.find(f)

            if not a:
                break

            pageno += 1

            z = re.compile(r"__doPostBack\('([^']+)','([^']+)'")
            m = re.search(z, a['href'])

            self.br.select_form(predicate=select_form)

            ctl = self.br.form.find_control('ctl00$_refineSearch1$ButtonRefine')
            self.br.form.controls.remove(ctl)

            self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': m.group(1)})
            self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': m.group(2)})
            self.br.form.new_control('hidden', '__LASTFOCUS',     {'value': ''})
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
            d = s.find('div', id='detail-page')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return LedcorJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
