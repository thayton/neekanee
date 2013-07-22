import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tekelec',
    'hq': 'Morrisville, NC',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.tekelec.com',
    'jobs_page_url': 'http://www.jobvite.com/CompanyJobs/Careers.aspx?c=qJY9Vfwv&cs=97d9Vfw8&jvresize=http://www.tekelec.com/resources/site1/General/docs/frameresize.htm',

    'empcnt': [1001,5000]
}

class TekelecJobScraper(JobScraper):
    def __init__(self):
        super(TekelecJobScraper, self).__init__(COMPANY)

    def new_url(self, url, jobid):
        u = urlparse.urlparse(url)
        l = urlparse.parse_qsl(u.query)
        x = dict(l)
        x.pop('cs')

        x['page'] = 'Job Description'
        x['j'] = jobid

        u = list(u)
        u[4] = urllib.urlencode(x)
        u = urlparse.urlunparse(u)

        return u

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r"jvGoToPage\('Job Description','','(.*)'\)")

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')
        
            l = self.parse_location(td[-1].text)
            if not l:
                continue

            m = re.search(r, a['href'])
            jobid = m.group(1)

            # http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qJY9Vfwv&jvresize=http%3a%2f%2fwww.tekelec.com%2fresources%2fsite1%2fGeneral%2fdocs%2fframeresize.htm&page=Job%20Description&j=orzWWfwC

            job = Job(company=self.company)
            job.title = a.text
            job.url = self.new_url(self.br.geturl(), jobid)
            job.location = l
            jobs.append(job)
            break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('form', attrs={'name': 'jvform'})

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return TekelecJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
