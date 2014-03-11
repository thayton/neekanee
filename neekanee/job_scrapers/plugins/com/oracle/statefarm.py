import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

COMPANY = {
    'name': 'State Farm',
    'hq': 'Bloomington, IL',

    'home_page_url': 'http://www.statefarm.com',
    'jobs_page_url': 'https://careers.statefarm.com',

    'bptw_glassdoor': True,

    'empcnt': [10001]
}

#
# https://online2.statefarm.com/apps/careers/psc/cgprdext/RECRUITING/EREC_EXT/c/HRS_HRAM.HRS_CE.GBL?Page=HRS_CE_JOB_DTL_SFI&Action=A&SiteId=1&PostingSeq=2&JobOpeningId=31140
#
# Base:  https://online2.statefarm.com/apps/careers/psc/cgprdext/RECRUITING/EREC_EXT/c/HRS_HRAM.HRS_CE.GBL
# Query: Page=HRS_CE_JOB_DTL_SFI&Action=A&SiteId=1&PostingSeq=2&JobOpeningId=31140
#
class StateFarmJobScraper(JobScraper):
    def __init__(self):
        super(StateFarmJobScraper, self).__init__(COMPANY)
        self.br.set_handle_redirect(False)
        import cookielib
        cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(cj)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text='Search Jobs'))

        s = soupify(self.br.response().read())

        #
        # We are now at a Javascript redirect page that
        # takes the URL argument of sfcgstart.html and 
        # replaces the string EMPLOYEE with the string 
        # recruiting:
        #
        #   function redir() {
        #     var url = new String(window.location.toString());
        #     ...
        #     qloc[1] = qloc[1].replace("EMPLOYEE", "RECRUITING");
        #     ...
        #   }
        #
        # The relevant part of the current URL looks like:
        #
        #   https://online2.statefarm.com/apps/careers/cgprdext/sfcgstart.html?https://online2.statefarm.com/.../EMPLOYEE/...
        #
        # and we redirect to
        #
        #   https://online2.statefarm.com/.../RECRUITING/...
        #
        l = self.br.geturl().split('?')
        l = l[1]
        l = re.sub(r'/EMPLOYEE/', '/RECRUITING/', l)

        try:
            self.br.open(l)
        except:
            # This document has moved temporarily...
            info = self.br.response().info()
            self.br.open(info['location'])

        s = soupify(self.br.response().read())
        i = s.find('input', id='HRS_APP_SRCHDRV_HRS_SEARCH_BTN')

        self.br.select_form('win0')
        self.br.form.set_all_readonly(False)
        self.br.form['ICAction'] = i['name']
        try:
            self.br.submit()
        except:
            self.br.open(self.br.response().info()['location'])

        s = soupify(self.br.response().read())
        i = s.find('input', attrs={'value': 'Search'})

        self.br.select_form('win0')
        self.br.form.set_all_readonly(False)
        self.br.form['ICAction'] = i['name']
        self.br.submit()

        r = re.compile(r'SCH_JOB_TITLE_LINK\$\d+')

        self.company.job_set.all().delete()

        while True:
            s = soupify(self.br.response().read())
            f = s.find('form', attrs={'name': 'win0'})

            for a in s.findAll('a', id=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[-1].text)
                
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text

                # from linkup inspection
                base = 'https://online2.statefarm.com/apps/careers/psc/cgprdext/RECRUITING/EREC_EXT/c/HRS_HRAM.HRS_CE.GBL'
                query = 'Page=HRS_CE_JOB_DTL_SFI&Action=A&SiteId=1&PostingSeq=2&JobOpeningId=%d' % int(td[3].text)

                job.url = base + '?' + query
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            x = re.compile(r'HRS_AGNT_RSLT_I\$hdown\$0')
            n = s.find('a', id=x)

            if n is None:
                break

            self.br.select_form('win0')
            self.br.form.set_all_readonly(False)
            self.br.form['ICAction'] = n['name']
            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            g = soupify(self.br.response().read())

            job.desc = get_all_text(g)
            job.save()

def get_scraper():
    return StateFarmJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
