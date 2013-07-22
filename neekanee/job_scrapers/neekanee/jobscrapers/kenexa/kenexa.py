import re, time, urllib, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

class KenexaJobScraper(JobScraper):
    def __init__(self, company_dict, location_handler=None):
        super(KenexaJobScraper, self).__init__(company_dict)
        self.soupify_search_form = False

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

    def update_frmAgent_form(self):
        """
        Derived classes should override in order to set any controls in
        frmAgent form prior to submitting the form. Form will already be
        selected when this method is invoked.
        """
        pass

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        if hasattr(self, 'follow_search_openings_link'):
            self.follow_search_openings_link()
        else:
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

        self.br.select_form('frmAgent')
        self.update_frmAgent_form()
        self.br.submit()

        r = re.compile(r'^cim_jobdetail\.asp')

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                if not tr:
                    continue

                td = tr.findAll('td')

                job = Job(company=self.company)
                job.location = self.company.location

                if hasattr(self, 'get_title_from_td'):
                    job.title = self.get_title_from_td(td)
                else:
                    job.title = a.text

                if hasattr(self, 'get_location_from_td'):
                    y = self.get_location_from_td(td)
                    if y is None:
                        continue

                    job.location = y

                job.url = self.mkurl(urlparse.urljoin(self.br.geturl(), a['href']))
                jobs.append(job)

            # Navigate to the next page
            try:
                n = self.br.find_link(text='Next')
                m = re.search(r'(\d+)', n.url)
            except mechanize.LinkNotFoundError:
                break

            self.br.select_form('frmMassSelect')
            self.br.form.set_all_readonly(False)
            self.br.form['recordstart'] = m.group(0)
            self.br.submit()

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

            a = {'name': 'frmJobDetail'}
            f = s.find('form', attrs=a)

            job.desc = get_all_text(f)
            job.save()
