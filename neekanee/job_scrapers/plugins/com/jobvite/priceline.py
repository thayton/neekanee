import re, urllib, urlparse
import HTMLParser

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from BeautifulSoup import BeautifulSoup

from neekanee_solr.models import *

COMPANY = {
    'name': 'Priceline.com',
    'hq': 'Norwalk, CT',

    'home_page_url': 'http://www.priceline.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qck9Vfwk&jvresize=http://www.priceline.com/careers/content/FrameResize.html&cs=91faVfw5&nl=0&page=Jobs',

    'empcnt': [5001,10000]
}

class PricelineJobScraper(JobScraper):
    def __init__(self):
        super(PricelineJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r"jvurlargs = '(.*)';")
        m = re.search(r, s.prettify())

        jvurlargs = m.group(1)
        jvurlargs = HTMLParser.HTMLParser().unescape(jvurlargs)

        x = {'class': 'jobList'}
        y = {'class': 'location'}
        d = s.find('div', attrs=x)
        r = re.compile(r"jvGoToPage\('(.*)','','(.*)'\)")

        for a in d.findAll('a', href=r):
            l = a.findParent('li')
            p = l.find('span', attrs=y)
            l = self.parse_location(p.text)
            
            if not l:
                continue

            m = re.search(r, a['href'])
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
            d = s.find('div', attrs={'class': 'jvcontent'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return PricelineJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
