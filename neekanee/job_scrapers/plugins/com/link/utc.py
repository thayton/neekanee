import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'United Technologies',
    'hq': 'Hartford, CT',

    'home_page_url': 'http://www.utc.com',
    'jobs_page_url': 'http://careers.utc.com',

    'empcnt': [10001]
}

class UtcJobScraper(JobScraper):
    def __init__(self):
        super(UtcJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        attempt = 0

        self.br.open(url)
        s = soupify(self.br.response().read())

        html = s.prettify()
        resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                       self.br.geturl(), 200, "OK")
        self.br.set_response(resp)
        self.br.select_form(nr=0)
        self.br.submit()

        r = re.compile(r'^/jobs/descriptions/[^/]+$')
        x = {'class': 'job-detail-jobtitle-link', 'href': r}

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[-1].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = td[1].a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            f = lambda x: x.name == 'a' and x.text == 'Next'
            a = s.find(f)

            if not a:
                break

            r = re.compile(r"doPostBack\('([^']+)")
            m = re.search(r, a['href'])

            html = s.prettify()
            resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                           self.br.geturl(), 200, "OK")

            def select_form(form):
                return form.attrs.get('id', None) == 'form1'

            self.br.set_response(resp)
            self.br.select_form(predicate=select_form)

            ctl = self.br.form.find_control('maincontent_0$rightcolcontent_1$findjob')
            self.br.form.controls.remove(ctl)

            ctl = self.br.form.find_control('maincontent_0$rightcolcontent_1$BusinessUnits')
            self.br.form.controls.remove(ctl)

            ctl = self.br.form.find_control('maincontent_0$rightcolcontent_5$btnSubscribe')
            self.br.form.controls.remove(ctl)

            self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': m.group(1)})
            self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
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
            d = s.find('div', id='jobDescriptionPage')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return UtcJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
