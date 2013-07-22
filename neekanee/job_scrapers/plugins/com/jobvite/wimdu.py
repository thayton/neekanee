import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from BeautifulSoup import BeautifulSoup

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wimdu',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.wimdu.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qZh9Vfw4&cs=9N8aVfwK',

    'empcnt': [201,500],
}

class WimduJobScraper(JobScraper):
    def __init__(self):
        super(WimduJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r"jvurlargs = '(.*)';")
        m = re.search(r, s.prettify())

        jvurlargs = m.group(1)

        v = { 'class': 'jobList' }
        d = s.find('div', attrs=v)
        r = re.compile(r"jvGoToPage\('(.*)','','(.*)'\)")

        for a in d.findAll('a', attrs={'href': r}):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[-1].text
            l = self.parse_location(l)
            
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
            f = s.find('form', id='jvform')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return WimduJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
