import re, urlparse

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SecondMarket',
    'hq': 'New York, NY',

    'ats': 'Jobvite',

    'contact': 'careers@SecondMarket.com',

    'home_page_url': 'http://www.secondmarket.com',
    'jobs_page_url': 'https://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qu39Vfwl&jvresize=https://www.secondmarket.com/iframe/resize/frame-resize',

    'empcnt': [51,200]
}

class SecondMarketJobScraper(JobScraper):
    def __init__(self):
        super(SecondMarketJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r'job\?jvi=\w+')
        d = { 'class': 'jvjoblink', 'href': r }

        for a in s.findAll('a', attrs=d):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = tr.find('td', attrs={'class': 'jvlocation'})
            l = re.sub(',\s*United States', '', l.text)
            l = self.parse_location(l)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = a['href']
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
            x = job.url.find('jvi=')
            j = '&j=' + job.url[x+4:]
            l = s.iframe['src'] + j + '&k=Job'

            self.br.open(l)

            s = soupify(self.br.response().read())
            f = s.find('form', attrs={'name': 'jvform'})

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return SecondMarketJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
