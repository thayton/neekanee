import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'CMA CGM',
    'hq': 'Marseille, France',

    'home_page_url': 'http://www.cma-cgm.com',
    'jobs_page_url': 'https://global3.recruitmentplatform.com/syndicated/lay/jsoutputinitrapido.cfm?ID=QIWFK026203F3VBQB8MV4F6R7&component=lay9999_src350a&LG=EN&mask=cmaext&browserchk=no',

    'empcnt': [10001]
}

class CmaCgmJobScraper(JobScraper):
    def __init__(self):
        super(CmaCgmJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('action', None) == 'jsoutputinitrapido.cfm'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.form['Resultsperpage'] = ['50']
        self.br.submit('srcsubmit')

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='TableJobs')
            r = re.compile(r'^jsoutputinitrapido\.cfm\?\S+PostingID=\d+')
        
            for a in d.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[2].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            x = {'class': 'Lst-ResNav'}
            td = d.find('td', attrs=x)
            x = {'class': 'Lst-NavPage'}
            p = td.findAll('span', attrs=x)
            i = [ p.index(v) for v in p if not v.a ][0]

            if i == len(p) - 1:
                break

            u = urlparse.urljoin(self.br.geturl(), p[i+1].a['href'])
            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='JDescContent')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CmaCgmJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
