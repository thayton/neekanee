import re, urllib, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from unescape import unescape
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lone Star College System',
    'hq': 'The Woodlands, TX',

    'ats': 'Oracle',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.lonestar.edu',
    'jobs_page_url': 'https://hcm.lonestar.edu/tsdwzs32.html',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

class LonestarJobScraper(JobScraper):
    def __init__(self):
        super(LonestarJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TAMLogin')
        self.br.submit()
        self.br.follow_link(self.br.find_link(text='TAM'))

        s = soupify(self.br.response().read())
        r = re.compile(r'^POSTINGTITLE\$\d+$')
        x = {'id': r, 'name': r}

#        self.company.job_set.all().delete()

        for a in s.findAll('a', attrs=x):
            f = s.find('form', attrs={'name': 'win0'})
            f['ICAction'] = a['id']

            job = Job(company=self.company)
            job.title = a.text
            job.location = self.company.location
            job.url = urlparse.urljoin(self.br.geturl(), f['action'])
            job.url_data = urllib.urlencode({'ICAction': a['id']})
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            html = self.urlencoded_form_to_html_form(job.url, job.url_data)
            html = str(html) # Required!
            resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                           job.url, 200, "OK")

            self.br.set_response(resp)
            self.br.select_form(nr=0)
            self.br.submit()

            z = soupify(self.br.response().read())
            d = z.find('div', id='PAGECONTAINER')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return LonestarJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
