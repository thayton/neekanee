import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Deloitte',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.deloitte.com',
    'jobs_page_url': 'http://careers.deloitte.com/jobs/eng-global',

    'empcnt': [10001]
}

class DeloitteJobScraper(JobScraper):
    def __init__(self):
        super(DeloitteJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())

        html = s.prettify()
        resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                       self.br.geturl(), 200, "OK")

        self.br.set_response(resp)
        self.br.select_form('aspnetForm')
        self.br.form.new_control('hidden', '__EVENTTARGET',   {'value': ''})
        self.br.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
        self.br.form.new_control('hidden', '__LASTFOCUS',     {'value': ''})
        self.br.form.fixup()
        self.br.form['ctl00$content$PageResults'] = ['100']
        self.br.submit('ctl00$content$SubmitBtn')

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'job-title'}

            for td in s.findAll('td', attrs=x):
                a = td.a
                tr = td.findParent('tr')
                td = tr.findAll('td', recursive=False)[2]

                if td.tr:
                    l = '-'.join(['%s' % y.text for y in td.tr.findAll('td')])
                else:
                    td = td.parent.findAll('td')
                    l = td[-3].text + '-' + td[-1].text

                l = self.parse_location(l)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Next'))
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form', id='aspnetForm')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return DeloitteJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
