import re, urlparse, urllib

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_add

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ruckus Wireless',
    'hq': 'Sunnyvale, CA',

    'home_page_url': 'http://www.ruckuswireless.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qLk9VfwT&jvprefix=http%3a%2f%2fwww.ruckuswireless.com&jvresize=http%3a%2f%2fwww.ruckuswireless.com%2fcareer-resize.html&k=JobListing&v=1',

    'empcnt': [201,500]
}

class RuckusWirelessJobScraper(JobScraper):
    def __init__(self):
        super(RuckusWirelessJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r"jvurlargs = '(.*)';")
        m = re.search(r, s.prettify())

        jvurlargs = m.group(1)
        jvurlargs = url_query_add(jvurlargs, {'jvprefix': 'https://www.uTest.com'}.items())

        x = {'class': 'jvcontent'}
        t = s.find('table', attrs=x)
        r = re.compile(r"jvGoToPage\('(.*)','','(.*)'\)")
        x = {'onclick': r}

        for a in t.findAll('a', attrs=x):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-1].text)
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
            x = {'name': 'jvform'}
            f = s.find('form', attrs=x)

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return RuckusWirelessJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
