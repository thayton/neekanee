import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Spirent',
    'hq': 'Germantown, MD',

    'ats': 'VirtualEdge',
    'benefits': {
        'url': 'http://www.spirent.com/About-Us/Careers/Benefits_compensation.aspx',
        'vacation': []
    },

    'home_page_url': 'http://www.spirent.com',
    'jobs_page_url': 'http://www.spirent.com/about-us/careers/opportunities.aspx',

    'empcnt': [1001,5000]
}

class SpirentJobScraper(JobScraper):
    def __init__(self):
        super(SpirentJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(tag='iframe'))    
        self.br.select_form('frmSearch')
        self.br.submit()

        pageno = 2
        r = re.compile(r'index.cfm\?fuseaction=mExternal\.showJob')

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                if td[2].text.find('U.S.') == -1:
                    continue

                l = self.parse_location(td[4].text + ',' + td[3].text)
                
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.location = l
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = urlutil.url_query_del(job.url, 'CurrentPage')
                jobs.append(job)

            # Navigate to the next page
            try:
                p = r'returnToResults&CurrentPage=' + str(pageno)
                pageno += 1
                n = self.br.find_link(url_regex=p)
                self.br.follow_link(n)
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find(text=re.compile(r'Job Title:'))
            t = t.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return SpirentJobScraper()
