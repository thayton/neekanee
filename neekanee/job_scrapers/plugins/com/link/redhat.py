import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Red Hat',
    'hq': 'Westford, MA',

    'home_page_url': 'http://www.redhat.com',
    'jobs_page_url': 'http://jobs.redhat.com/job-search-results/',

    'empcnt': [1001,5000]
}

class RedHatJobScraper(JobScraper):
    def __init__(self):
        super(RedHatJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^/jobs/descriptions/')
            x = {'href': r, 'title': 'click for job details'}
        
            for a in s.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[-2].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            y = re.compile(r"__doPostBack\('([^']+)'")
            z = re.compile(r'^maincontent_\d+_jobsearchresults_\d+_next_page$')
            a = s.find(id=z)

            if not a:
                break

            m = re.search(y, a['href'])
            
            def select_form(form):
                return form.attrs.get('id', None) == 'form1'

            self.br.select_form(predicate=select_form)
            self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': m.group(1)})
            self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
            self.br.form.new_control('hidden', '__LASTFOCUS',     {'value': ''})
            self.br.form.fixup()

            # Next page doesn't seem to work unless we remove these controls
            for control in self.br.form.controls[:]:
                if control.type in ['image', 'checkbox']:
                    self.br.form.controls.remove(control)

            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'jobdetail-container'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return RedHatJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
