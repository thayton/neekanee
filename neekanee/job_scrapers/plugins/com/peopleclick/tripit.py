import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'TripIt',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.tripit.com',
    'jobs_page_url': 'http://careers.peopleclick.com/careerscp/client_concur/tripit/search.do',

    'empcnt': [11,50]
}

class TripItJobScraper(JobScraper):
    def __init__(self):
        super(TripItJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        self.company.job_set.all().delete()

        #
        # Some of script contents throw off mechanize
        # and it gives error 'ParseError: OPTION outside of SELECT'
        # So we soupify it to remove script contents
        #
        s = soupify(self.br.response().read())

        html = s.prettify()
        resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                       self.br.geturl(), 200, "OK")

        self.br.set_response(resp)
        self.br.select_form('searchForm')
        self.br.form.set_all_readonly(False)
        self.br.submit(id='searchButton')

        r = re.compile(r'^jobDetails\.do\?functionName=getJobDetail&jobPostId=\d+')
        pageno = 2

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')
            
                l = self.parse_location(td[-4].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            p = 'PARAMFILTER:functionName=search|pageIndex=%d|' % pageno
            b = s.find('input', attrs={'name': p})
            if not b:
                break

            self.br.select_form('searchResultForm')
            self.br.form.set_all_readonly(False)
            self.br.submit(name=b['name'])

            pageno += 1

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            try:
                self.br.open(job.url)
            except:
                continue

            s = soupify(self.br.response().read())
            a = {'name': 'jobDetails'}
            f = s.find('form', attrs=a)

            job.desc = get_all_text(f)    
            job.save()

def get_scraper():
    return TripItJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
