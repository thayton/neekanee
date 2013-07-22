import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'iDirect',
    'hq': 'Herndon, VA',

    'ats': 'submit4jobs',

    'home_page_url': 'http://www.idirect.net',
    'jobs_page_url': 'http://www.idirect.net/Company/Careers/Current-Positions.aspx',

    'empcnt': [201,500]
}

class iDirectJobScraper(JobScraper):
    def __init__(self):
        super(iDirectJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('jobsearchform')
        self.br.form.set_all_readonly(False)
        self.br.form['gojobsearch'] = '1'
        self.br.submit()

        pageno = 2

        while True:
            for l in self.br.links(url_regex=re.compile(r'viewjobdetail')):
                m = re.search(r'(.*)\W+\((.*)\)', l.text)
                x = self.parse_location(m.group(2))

                if x is None:
                    continue

                job = Job(company=self.company)
                job.title = m.group(1)
                job.location = x
                job.url = urlparse.urljoin(l.base_url, l.url)
                jobs.append(job)

            # Navigate to the next page
            try:
                p = r'gopage=' + str(pageno)
                pageno += 1
                n = self.br.find_link(url_regex=p)
                self.br.follow_link(n)
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
            d = s.find('div', attrs={'class': 'contentBody'})
            t = d.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return iDirectJobScraper()
