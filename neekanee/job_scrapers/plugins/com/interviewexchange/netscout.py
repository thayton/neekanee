import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

"""
oamSubmitForm(formName, linkId, target, params)

oamSubmitForm('bodyPage:jobSearchResultsForm',
              'bodyPage:jobSearchResultsForm:JobSearchResultsNavigationPageView:searchResultsDataTable:0:c2',
              null,
              [['conversationId','68651'],['conversationPropagation','begin']]
             )

document.forms['bodyPage:jobSearchResultsForm'].target = null
document.forms['bodyPage:jobSearchResultsForm'].conversationId = 68651
document.forms['bodyPage:jobSearchResultsForm'].conversationPropagation = begin
document.forms['bodyPage:jobSearchResultsForm'].bodyPage:jobSearchResultsForm:_idcl = bodyPage:jobSearchResultsForm:JobSearchResultsNavigationPageView:searchResultsDataTable:0:c2
"""

COMPANY = {
    'name': 'NetScout',
    'hq': 'Westford, MA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.netscout.com',
    'jobs_page_url': 'https://2xrecruit.kenexa.com/kr/cc/jsp/public/landingPage.jsf?id=C2F091320C5351B98CA4E3D110F65CA880C52774F4B4B4D81B444CA5FB49CAB3&initcc=true',

    'empcnt': [501,1000]
}

class NetScoutJobScraper(JobScraper):
    def __init__(self):
        super(NetScoutJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        '''
        Just pick up the requisition IDs here to see which jobs are new and
        which jobs we've already scraped.
        '''
        jobs = []

        self.br.open(url)
        self.br.select_form('bodyPage:jobSearchForm')
        self.br.submit('basicShowAllJobs')

        s = soupify(self.br.response().read())
        r = re.compile(r"return oamSubmitForm\('([^,]+)','([^,]+)',null,\[\['conversationId','(\d+)'\],\['conversationPropagation','begin'\]\]\)")
        t = re.compile(r'(https://\S+/EmailJobDetail\.jsf\?npi=[^&]+&amp;rand=[^&]+)')
        x = {'onclick': r}

        for a in s.findAll('a', attrs=x):
            m = re.search(r, a['onclick'])
            if not m:
                continue

            tr = a.findParent('tr').findParent('tr')
            td = tr.td.findAll('td')[1]

            job = Job(company=self.company)
            job.title = td.text

            formName = m.group(1)
            linkId = m.group(2)
            conversationId = m.group(3)

            self.br.select_form(formName)
            self.br.form.set_all_readonly(True)
            self.br.form.new_control('hidden', 'conversationId',    {'value':conversationId})
            self.br.form.new_control('hidden', formName + ':_idcl', {'value':linkId})
            self.br.submit()

            z = soupify(self.br.response().read())
            d = z.find('div', id=re.compile(r'jobDescription_contentWrapper'))

            if not d:
                d = z.find('form', id='bodyPage:jobDetail')
            if not d:
                continue

            job.desc = get_all_text(d)

            #
            # In order to get a clickable link for this job in Neekanee we have
            # to go the the 'Email this job to a friend' page for this page and
            # extract the link they give to us there
            #
            u = urlparse.urljoin(self.br.geturl(), 'emailFriend.jsf?conversationId='+conversationId)
            self.br.open(u)

            z = soupify(self.br.response().read())
            m = re.search(t, z.text)

            if not m:
                continue

            job.url = m.group(1).replace('&amp;', '&')
            
            self.br.open(job.url)
            z = soupify(self.br.response().read())

            location = [ z.find('label', id='bodyPage:jobDetail:CITYLabel'),
                         z.find('label', id='bodyPage:jobDetail:STATELabel'),
                         z.find('label', id='bodyPage:jobDetail:zipPostalLabel') ]

            l = '-'.join(['%s' % e.findParent('tr').findAll('td')[-1].text for e in location if e ])
            l = self.parse_location(l)

            if not l:
                continue
            
            job.location = l
            jobs.append(job)

            self.br.back()
            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)


def get_scraper():
    return NetScoutJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
