import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Raytheon',
    'hq': 'Waltham, MA',

    'home_page_url': 'http://www.raytheon.com',
    'jobs_page_url': 'http://jobs.raytheon.com/en/search/',

    'empcnt': [10001]
}

class RaytheonJobScraper(JobScraper):
    def __init__(self):
        super(RaytheonJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r'^/jobs/[^/]+$')
        x = {'href': r, 'title': True}

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='contentright_3_JobListContainer')

            for a in d.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = ', '.join(['%s' % t.text for t in td[2:5]])
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

            y = re.compile(r'^contentright_\d+_next_page$')
            z = re.compile(r"'(contentright_\d+\$next_page)'")
            a = s.find('a', id=y)

            if not a:
                break

            m = re.search(z, a['href'])

            def select_form(form):
                return form.attrs.get('id', None) == 'form1'

            self.br.select_form(predicate=select_form)
            self.br.form.set_all_readonly(False)
            self.br.form['ctl03_HiddenField'] = ';;AjaxControlToolkit, Version=3.5.50927.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:4a126967-c4d4-4d5c-8f94-b4e3e72d7549:5546a2b:475a4ef5:d2e10b12:effe2a26:37e2e5c9:5a682656:12bbc599'
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
            x = {'class': 'tblJobDetails'}
            d = s.find('div', attrs=x)
            d = d.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return RaytheonJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
