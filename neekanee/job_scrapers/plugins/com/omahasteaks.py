import re, urllib, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

COMPANY = {
    'name': 'Omaha Steaks',
    'hq': 'New York, NY',

    'benefits': {
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.omahasteaks.com',
    'jobs_page_url': 'https://partner.omahasteaks.com/hr/frontpage.jsp',

    'empcnt': [1001,5000]
}

class OmahaSteaksJobScraper(JobScraper):
    def __init__(self):
        super(OmahaSteaksJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        
        for form in self.br.forms():
            self.br.form = form
            self.br.form.set_all_readonly(False)
            self.br.submit()

            s = soupify(self.br.response().read())

            for view_post_form in self.br.forms():
                try:
                    postingid = view_post_form['postingid']
                except mechanize.ControlNotFoundError:
                    continue

                x = {'name': 'postingid', 'value': postingid}
                i = s.find('input', attrs=x)
                f = i.findParent('form')

                tr = i.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[3].text)
                
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = td[0].text
                job.url = urlparse.urljoin(self.br.geturl(), f['action'])
                job.url += '?postingid=%d' % int(postingid)
                job.location = l
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            m = soupify(self.br.response().read())
            d = m.find('div', id='maincontent')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return OmahaSteaksJobScraper()
