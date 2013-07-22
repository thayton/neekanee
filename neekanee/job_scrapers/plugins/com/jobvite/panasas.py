import re, urllib, urlparse

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Panasas',
    'hq': 'Fremont, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.panasas.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qO49VfwG&jvprefix=http%3a%2f%2fwww.panasas.com&jvresize=http%3a%2f%2fpantest.panasas.com%2fsites%2fdefault%2ffiles%2fFrameResize.html&k=JobListing&v=1',

    'empcnt': [51,200]
}

class PanasasJobScraper(JobScraper):
    def __init__(self):
        super(PanasasJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r"jvurlargs = '(.*)';")
        m = re.search(r, s.prettify())

        jvurlargs = m.group(1)

        t = s.find('table', attrs={'class': 'jvcontent'})
        r = re.compile(r"jvGoToPage\('(.*)','','(.*)'\)")

        for a in t.findAll('a', attrs={'onclick': r}):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[-1].text
            l = self.parse_location(l)

            if not l:
                continue

            m = re.search(r, a['onclick'])
            page  = m.group(1)
            jobid = m.group(2)

            job = Job(company=self.company)
            job.title = a.text
            job.url = self.mkurl(self.br.geturl(), jvurlargs, page, jobid)
            job.location = l
            jobs.append(job)

        return jobs

    def mkurl(self, url, jvurlargs, page, jobid):
        #
        # Do the same thing as jvGoToPage()
        #
        l = url[0:url.find('?')]
        l += jvurlargs + '&page=' + urllib.quote(page)
        l += '&j=' + jobid
        return l
    
    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            a = {'class': 'jvheader'}
            d = s.find('div', attrs=a)
            t = d.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return PanasasJobScraper()
