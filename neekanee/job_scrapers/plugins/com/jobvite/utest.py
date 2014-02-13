import re, urlparse, urllib

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_add

from neekanee_solr.models import *

COMPANY = {
    'name': 'uTest',
    'hq': 'Framingham, MA',

    'home_page_url': 'https://www.utest.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?k=JobListing&c=qyH9Vfw3&v=1&jvresize=/sites/all/themes/uTestX/includes/CareersPageFrameResize.html',

    'empcnt': [51,200]
}

class uTestJobScraper(JobScraper):
    def __init__(self):
        super(uTestJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r"jvurlargs = '(.*)';")
        m = re.search(r, s.prettify())

        jvurlargs = m.group(1)
        jvurlargs = url_query_add(jvurlargs, {'jvprefix': 'https://www.uTest.com'}.items())

        x = {'class': 'jvlisting'}
        d = s.find('div', attrs=x)
        r = re.compile(r"jvGoToPage\('(.*)','','(.*)'\)")
        x = {'onclick': r}
        y = {'class': 'joblocation'}

        for a in d.findAll('a', attrs=x):
            p = a.findParent('li')
            p = p.find('span', attrs=y)
            l = self.parse_location(p.text)

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
            a = {'class': 'jvcontent'}
            d = s.find('div', attrs=a)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return uTestJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
