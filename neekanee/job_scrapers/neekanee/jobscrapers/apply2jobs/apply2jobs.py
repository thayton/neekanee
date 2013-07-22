import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

class Apply2JobsJobScraper(JobScraper):
    def __init__(self, company_dict):
        company_dict['ats'] = 'Apply2Jobs'
        super(Apply2JobsJobScraper, self).__init__(company_dict)
        self.soupify_search_form = False

    def update_frmSearch_form(self):
        """
        Derived classes should override in order to set any controls in
        frmSearch form prior to submitting the form. Form will already be
        selected when this method is invoked.
        """
        pass

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

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

        self.br.select_form(name='frmSearch')
        self.update_frmSearch_form()
        self.br.submit()

        r = re.compile(r'index.cfm\?fuseaction=mExternal\.showJob')
        v = { 'class': 'SearchResults', 'href': r }

        pageno = 2
    
        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', attrs=v):
                tr = a.findParent('tr')
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
            a = {'class': 'JobDetailTable'}
            t = s.find('table', attrs=a)

            if hasattr(self, 'get_location_from_desc'):
                y = self.get_location_from_desc(s)
                if y is None:
                    continue

                job.location = y

            job.desc = get_all_text(t)
            job.save()
