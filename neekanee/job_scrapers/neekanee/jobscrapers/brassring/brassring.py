import re, time, urllib, urlparse, mechanize, urlutil, json

from neekanee import urlutil
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

class BrassringJobScraper(JobScraper):
    def __init__(self, company_dict, location_handler=None):
        super(BrassringJobScraper, self).__init__(company_dict)
        self.soupify_search_form = False
        self.use_company_location = False # Default to company location for jobs

    def mkurl(self, job_link):
        """
        Query portion of the url returned looks like this:

        cim_jobdetail.asp?jobId=1212739&siteId=69&partnerid=119

        Full url eg:

        https://sjobs.brassring.com/en/asp/tg/cim_jobdetail.asp?jobId=1212739&siteId=69&partnerid=119
        """
        items = urlutil.url_query_get(self.company.jobs_page_url.lower(), ['partnerid', 'siteid'])

        url = urlutil.url_query_filter(job_link, 'jobId')
        url = urlutil.url_query_add(url, items.iteritems())

        return url

    def update_aspnetForm_form(self):
        """
        Derived classes should override in order to set any controls in
        aspnetForm form prior to submitting the form. Form will already be
        selected when this method is invoked.
        """
        pass

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text_regex=re.compile(r'Search openings', re.I)))

        if self.soupify_search_form:
            #
            # Some of script contents throw off mechanize
            # and it gives error 'ParseError: OPTION outside of SELECT'
            # So we soupify it to remove script contents
            #
            s = soupify(self.br.response().read())

            html = s.prettify()
            resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                           self.br.geturl(), 200, "OK")
            self.br.set_response(resp)

        self.br.select_form('aspnetForm')
        self.br.form.new_control('hidden', 'submit2', {'value':''})
        self.br.form.new_control('hidden', 'GTGLanguageList', {'value':'1||1033'})
        self.update_aspnetForm_form()
        self.br.submit()

        r = re.compile(r'^jobdetails\.asp')
        numResults = 0

        while True:
            s = soupify(self.br.response().read())
            i = s.find('input', id='ctl00_MainContent_GridFormatter_json_tabledata')
            j = json.loads(i['value'])

            for x in j:
                job = Job(company=self.company)

                if hasattr(self, 'get_title_from_formtext'):
                    job.title = self.get_title_from_formtext(x)
                else:
                    job.title = a.text

                if self.use_company_location:
                    job.location = self.company.location

                if hasattr(self, 'get_location_from_formtext'):
                    y = self.get_location_from_formtext(x)
                    if y is None:
                        continue

                    job.location = y

                if hasattr(self, 'get_url_from_formtext'):                    
                    a = self.get_url_from_formtext(x)
#                    a = soupify(self.get_url_from_formtext(x)).a


                job.url = self.mkurl(urlparse.urljoin(self.br.geturl(), a['href']))
                jobs.append(job)

            numResults += len(j)

            if self.soupify_search_form:
                f = s.find('form', attrs={'name': 'frmMassSelect'})
                html = f.prettify()
                resp = mechanize.make_response(html, [("Content-Type", "text/html")],
                                               self.br.geturl(), 200, "OK")
                self.br.set_response(resp)

            self.br.select_form('frmMassSelect')

            if numResults >= int(self.br.form['totalrecords']):
                break

            self.br.form.set_all_readonly(False)
            self.br.form['recordstart'] = '%d' % (numResults + 1)

            try:
                self.br.submit()
            except:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())

            if hasattr(self, 'get_location_from_desc'):
                y = self.get_location_from_desc(s)
                if y is None:
                    continue

                job.location = y

            d = s.find('div', id='PrimaryContentBlock')
            t = d.findParent('table')

            if t:
                job.desc = get_all_text(t)
            else:
                job.desc = get_all_text(d)

            job.save()
