import re
import urllib
import urlutil
import httplib
import urlparse
import mechanize

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

class PeopleAdminJobScraper(JobScraper):
    """ Crawler for the PeopleAdmin Applicant Tracking System """
    def __init__(self, company_dict):
        self.link_text = 'Search Postings'
        company_dict['ats'] = 'PeopleAdmin'
        super(PeopleAdminJobScraper, self).__init__(company_dict)

    def get_job_cmp(self):
        """
        Compare jobs without the 'c' and 'windowTimestamp' fields included in 
        the comparison. Do a dictionary comparison since the urls might be
        equivalent but look different because the query params are in a different
        order in url1 vs url2
        """
        def job_cmp(job1, job2):
            url1 = urlutil.url_query_del(job1.url, ['c', 'windowTimestamp'])
            url2 = urlutil.url_query_del(job2.url, ['c', 'windowTimestamp'])

            url1_qs = urlparse.parse_qs(urlparse.urlparse(url1).query)
            url2_qs = urlparse.parse_qs(urlparse.urlparse(url2).query)

            return url1_qs == url2_qs

        return job_cmp

    def update_hrSearch_form(self):
        """
        Derived classes should override in order to set any controls in
        hrSearch form prior to submitting the form. Form will already be
        selected when this method is invoked.
        """
        pass

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        t = s.find('script').text
        r = re.compile(r'location\.replace\(\'(.*)\'')
        m = re.search(r, t)
        u = urlparse.urljoin(self.br.geturl(), m.group(1))

        self.br.open(u)

        s = BeautifulSoup(self.br.response().read())
        f = s.find('frame', src=re.compile(r'Nav\.jsp'))
        u = urlparse.urljoin(self.br.geturl(), f['src'])

        self.br.open(u)

        self.br.select_form('navForm')
        self.br.form.set_all_readonly(False)
        self.br.form['searchType'] = '8192'
        self.br.form['delegateParameter'] = 'searchDelegate'
        self.br.form['actionParameter'] = 'showSearch'
        self.br.submit()

        s = BeautifulSoup(self.br.response().read())
        t = s.find('script').text
        m = re.search(r, t)
        u = urlparse.urljoin(self.br.geturl(), m.group(1))

        self.br.open(u)

        self.br.select_form('hrSearch')
        self.br.form.set_all_readonly(False)
        self.br.form['searchType'] = '8192'
        self.br.form['delegateParameter'] = 'searchDelegate'
        self.br.form['actionParameter'] = 'goSearch'
        self.update_hrSearch_form()
        self.br.submit()

        while True:
            s = BeautifulSoup(self.br.response().read())
            t = s.find('script').text
            m = re.search(r, t)
            u = urlparse.urljoin(self.br.geturl(), m.group(1))

            self.br.open(u)

            s = BeautifulSoup(self.br.response().read())
            v = { 'action': '/applicants/Central', 'name': re.compile(r'^link_') }

            for f in s.findAll('form', attrs=v):
                b = f.findPrevious('b')

                tr = b.findPrevious('tr')
                td = tr.findAll('td')

                job = Job(company=self.company)

                if hasattr(self, 'get_title_from_td'):
                    job.title = self.get_title_from_td(td)
                else:
                    job.title = b.text

                url = urlparse.urljoin(self.br.geturl(), f['action'])
                url += '?' + urllib.urlencode(extract_form_fields(f))

                job.url = url
                job.location = self.company.location

                if hasattr(self, 'get_location_from_td'):
                    y = self.get_location_from_td(td)
                    if y is None:
                        continue

                    job.location = y

                jobs.append(job)

            # Navigate to the next page
            p = re.compile(r'^Next Page')
            n = s.find(text=p)
            if n is None:
                break

            f = n.findParent('form')
            self.br.select_form(f['name'])
            self.br.form.set_all_readonly(False)
            self.br.form['delegateParameter'] = 'functionalityTableDelegate'
            self.br.form['actionParameter'] = 'getNextRowSet'
            self.br.submit()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list, use_job_cmp=True)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            x = BeautifulSoup(self.br.response().read())

            t = x.find('script').text
            r = re.compile(r'location\.replace\(\'(.*)\'')
            m = re.search(r, t)
            u = urlparse.urljoin(self.br.geturl(), m.group(1))

            self.br.open(u)

            x = soupify(self.br.response().read())
            t = x.find(text='Position Information')

            if t is None:
                t = x.find(text='Posting Details')
            if t is None:
                t = x.find(text='Posting Number:')                

            tr = t.findNext('tr')

            job.desc = get_all_text(tr)

            #
            # XXX Remove the 'c' and 'windowTimestamp' fields from the url
            # before saving. We need these otherwise the call to self.br.open(job.url)
            # returns the wrong results (dunno why). But we don't want these fields
            # in the final result that the user clicks on.
            #
            job.url = urlutil.url_query_del(job.url, ['c', 'windowTimestamp'])
            job.save()
