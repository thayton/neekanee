import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Trinity College Dublin',
    'hq': 'Dublin, Ireland',

    'home_page_url': 'http://www.tcd.ie',
    'jobs_page_url': 'https://jobs.tcd.ie/pls/corehrrecruit/erq_search_package.search_form?p_company=1&p_internal_external=E#',

    'empcnt': [201,500]
}

class TcdJobScraper(JobScraper):
    def __init__(self):
        super(TcdJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        pageno = 2

        self.br.open(url)
        self.br.select_form('callErecruitDoSearch')
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r"viewTheJobSpec\('(\d+)'\)")
            x = {'class': 'erq_searchv4_big_anchor', 'href': r}

            for a in s.findAll('a', attrs=x):
                m = re.search(r, a['href'])

                job = Job(company=self.company)
                job.title = a.text
                job.location = self.company.location

                self.br.select_form('callTheJobSpecFromSearch')
                self.br.form.set_all_readonly(False)
                self.br.form['p_recruitment_id'] = m.group(1)
                self.br.submit()

                z = soupify(self.br.response().read())
                y = re.compile(r'view_erecruit_document\?p_key_\d+=')
                a = z.find('a', href=y)

                if not a:
                    continue

                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                jobs.append(job)

                self.br.back()

            f = lambda x: x.name == 'a' and x.text == 'Next'
            a = s.find(f)

            if not a:
                break

            self.br.select_form('searchv4navigateresultsforward')
            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return TcdJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
