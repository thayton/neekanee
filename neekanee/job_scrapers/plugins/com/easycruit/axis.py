import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Axis Communications',
    'hq': 'Chelmsford, MA',

    'ats': 'EasyRecruit',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.axis.com',
    'jobs_page_url': 'http://axis.easycruit.com/',

    'empcnt': [1001,5000]
}

class AxisJobScraper(JobScraper):
    def __init__(self):
        super(AxisJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('job_search')
        self.br.set_all_readonly(False)
        self.br.form['search_area_of_interest'] = ['27596'] # usa
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r"window\.open\('(/vacancy/\d+/\d+\?iso=gb)'")

        for a in s.findAll('a', href=r):
            m = re.search(r, a['href'])
            u = m.group(1)

            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[1].text)
            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), u)
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('td', attrs={'class': 'vacancy'})

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return AxisJobScraper()
