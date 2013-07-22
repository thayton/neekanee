import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'CEDA International Corporation',
    'hq': 'Calgary, Canada',

    'home_page_url': 'http://www.cedagroup.com',
    'jobs_page_url': 'http://www.cedagroup.com/common/careers.nsf/vwHTMLInternetJobPostings!OpenView&BaseTarget=MainRight',

    'empcnt': [1001,5000]
}

class CedaJobScraper(JobScraper):
    def __init__(self):
        super(CedaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'listing-job-title'}
        y = {'class': 'listing-location'}
        r = re.compile(r"openChild\('([^']+)")

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-7].text)
            if not l:
                continue

            # function openChild(docID) {
            #   window.open(dbPath + "/$defaultView/" + docID + "?OpenDocument&id=" + Math.round(200 * Math.random()), app, "resizable,scrollbars,left=50,width=820")
            # }
            m = re.search(r, a['href'])
            p = '/common/careers.nsf/$defaultView/' + m.group(1) + '?OpenDocument'
            u = urlparse.urljoin(self.br.geturl(), p)

            job = Job(company=self.company)
            job.title = a.text
            job.url = u
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
            f = s.form

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return CedaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
