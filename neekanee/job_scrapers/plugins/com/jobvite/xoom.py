import re, urlparse, urllib

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_add

from neekanee_solr.models import *

COMPANY = {
    'name': 'Xoom',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'contact': 'resumes@xoom.com',

    'home_page_url': 'https://www.xoom.com',
    'jobs_page_url': 'https://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qB49Vfwt&cs=9uoaVfwH&jvresize=https://www.xoom.com/about/iframe-resizer',
#    'jobs_page_url': 'https://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qB49Vfwt&jvprefix=https%3a%2f%2fwww.xoom.com&cs=9Tv9Vfwc&jvresize=https%3a%2f%2fwww.xoom.com%2fabout%2fjobvite-iframe-resizer',

    'empcnt': [51,200]
}

class XoomJobScraper(JobScraper):
    def __init__(self):
        super(XoomJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r"jvurlargs = '(.*)';")
        m = re.search(r, s.prettify())

        jvurlargs = m.group(1)
        jvurlargs = url_query_add(jvurlargs, {'jvprefix': 'https://www.xoom.com'}.items())

        d = s.find('div', attrs={'class': 'jobList'})
        r = re.compile(r"jvGoToPage\('(.*)','','(.*)'\)")

        for a in d.findAll('a', href=r):
            m = re.search(r, a['href'])
            page  = m.group(1)
            jobid = m.group(2)
        
            job = Job(company=self.company)
            job.title = a.text
            job.url = self.mkurl(self.br.geturl(), jvurlargs, page, jobid)
            job.location = self.company.location
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
    return XoomJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
