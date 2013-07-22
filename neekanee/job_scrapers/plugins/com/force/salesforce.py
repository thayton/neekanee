import re, urlparse
import mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee_solr.models import *

COMPANY = {
    'name': 'SalesForce',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.salesforce.com',
    'jobs_page_url': 'http://careers.force.com/jobs',

    'empcnt': [1001,5000]
}

# XXX like enterasys
class SalesForceJobScraper(JobScraper):
    def __init__(self):
        super(SalesForceJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        f = None
        jobs = []

        def select_form(form):
            if form.attrs.has_key('action'):
                return form.attrs['action'] == '/jobs/ts2__JobSearch'

            return False

        self.br.open(url)

        s = soupify(self.br.response().read())

        view_state = s.find('input', id='com.salesforce.visualforce.ViewState')
        view_state_mac = s.find('input', id='com.salesforce.visualforce.ViewStateMAC')

        self.br.select_form(predicate=select_form)
        self.br.form.new_control('hidden', 'com.salesforce.visualforce.ViewState',   {'value':''})
        self.br.form.new_control('hidden', 'com.salesforce.visualforce.ViewStateMAC', {'value':''})
        self.br.form.fixup()

        self.br.form.set_all_readonly(False)
        self.br.form['com.salesforce.visualforce.ViewState'] = view_state['value']
        self.br.form['com.salesforce.visualforce.ViewStateMAC'] = view_state_mac['value']

        self.br.submit()

        pageno = 1

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'/jobs/ts2__JobDetails\?jobId=\w+')
        
            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[-1].text.lower().strip()

                if l.find('anywhere') != -1:
                    continue

                l = self.parse_location(l)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.location = l
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                jobs.append(job)

            # Do AJAX request/replacement manually for search form
            if not f:
                z = s.findAll('form', attrs={'action': '/jobs/ts2__JobSearch'})
                for y in z:
                    if y['name'].endswith('atsSearch'):
                        y.extract()

                f = z.pop()
            else:
                ajax = s.find('span', id='ajax-view-state')
                ajax_viewstate = ajax.find('input', id='com.salesforce.visualforce.ViewState')
                ajax_viewstatemac = ajax.find('input', id='com.salesforce.visualforce.ViewStateMAC')
                ajax_nextpage = s.find(lambda x: x.name == 'a' and x.text == 'Next&gt;')

                if ajax_nextpage is None:
                    # On the last page
                    break

                f_viewstate = f.find('input', id='com.salesforce.visualforce.ViewState')
                f_viewstatemac = f.find('input', id='com.salesforce.visualforce.ViewStateMAC')
                f_nextpage = f.find(lambda x: x.name == 'a' and x.text == 'Next&gt;')

                f_viewstate.replaceWith(ajax_viewstate)
                f_viewstatemac.replaceWith(ajax_viewstatemac)
                f_nextpage.replaceWith(ajax_nextpage)

            resp = mechanize.make_response(f.prettify(), [("Content-Type", "text/html")],
                                           self.br.geturl(), 200, "OK")
            self.br.set_response(resp)

            if pageno >= 15:
                print "break"

            l = self.br.find_link(text='Next>')
            x = l.attrs[2][1]

            def select_next_form(form):
                if form.attrs.has_key('action'):
                    if form.attrs['action'] == '/jobs/ts2__JobSearch' and \
                            not form.name.endswith('atsSearch'):
                        return True

                    return False

            self.br.select_form(predicate=select_next_form)
            self.br.form.new_control('hidden', 'AJAXREQUEST', {'value': '_viewRoot'})
            self.br.form.new_control('hidden', x, {'value': x})
            self.br.form.fixup()
            self.br.submit()

            print 'Page ',pageno
            pageno += 1

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            try:
                self.br.open(job.url)
            except:
                print 'self.br.open(%s) failed' % job.url
                continue

            s = soupify(self.br.response().read())
            x = {'class': 'atsJobDetailsTable'}
            t = s.find('table', attrs=x)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return SalesForceJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
