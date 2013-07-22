import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'eEye Digital Security',
    'hq': 'Irvine, CA',

    'ats': 'Taleo',

    'contact': 'hr@eEye.com',

    'home_page_url': 'http://www.eeye.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA4/ats/careers/jobSearch.jsp?org=EEYEDIGITALSECURITY&cws=1',

    'empcnt': [51,200]
}

class eEyeJobScraper(JobScraper):
    def __init__(self):
        super(eEyeJobScraper, self).__init__(COMPANY)
    
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        s = soupify(self.br.response().read())
    
        for a in s.findAll('a', href=re.compile(r'requisition\.jsp')):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[-1].text

            #
            # Handle 'Irvine, CA OR Phoenix, AZ'
            #
            if l.find(',') != l.rfind(','):
                l = l.split(',')[0] + ',' + \
                    l.split(',')[1].split()[0]

            l = self.parse_location(l)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.location = l
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = urlutil.url_params_del(job.url)
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='main')
            x = {'class': 'post-holder'}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return eEyeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
