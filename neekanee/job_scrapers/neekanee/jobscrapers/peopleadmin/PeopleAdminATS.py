import re
import sys
import httplib
import urllib
import urlparse
import mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, unescape

from neekanee_solr.models import *

class PeopleAdminJobScraper(JobScraper):
    def __init__(self, company_dict):
        company_dict['ats'] = 'PeopleAdmin'
        self.link_text = 'Search Postings'
        super(PeopleAdminJobScraper, self).__init__(company_dict)

    def make_job_link(self, url):
        """
        Trim down the link to only keep the essential query parameters that
        we need.

        => From:

        https://jobs.princeton.edu/applicants/Central?delegateParameter=applicantPostingSearchDelegate&actionParameter=getJobDetail&rowId=186162&c=fqj1RhxKAmwl%2BdiRLAdMLg%3D%3D&pageLoadIdRequestKey=1328027125126&functionalityTableName=8192&windowTimestamp=PA_1328027122188

        => To:

        https://jobs.princeton.edu/applicants/Central?delegateParameter=applicantPostingSearchDelegate&actionParameter=getJobDetail&rowId=186162
        """
        o = urlparse.urlparse(url)
        qs = o.query
        qd = urlparse.parse_qs(qs)

        del(qd['c'])
        del(qd['windowTimestamp'])
        del(qd['functionalityTableName'])
        del(qd['pageLoadIdRequestKey'])

        query = urllib.urlencode(qd, doseq=True)
        parse_result = urlparse.ParseResult(o.scheme,
                                            o.netloc,
                                            o.path,
                                            o.params,
                                            query,
                                            o.fragment)
        newurl = urlparse.urlunparse(parse_result)
        return newurl

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
        self.br.follow_link(self.br.find_link(text=self.link_text))
        self.br.select_form('hrSearch')
        self.update_hrSearch_form()
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            s = s.find('table', attrs={'summary': 'Search Results'})

            if not s:
                break

            for t in s.findAll(text='View'):
                a = t.parent
                x = a.findParent('td')

                job = Job(company=self.company)
                job.title = x.contents[0].strip()
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = self.make_job_link(job.url)

                jobs.append(job)

            # Navigate to the next page
            try:
                r = re.compile(r'^Next Page')
                n = self.br.find_link(text_regex=r)
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
            x = {'class': 'displayItemsGroup'}
            d = s.find('div', attrs=x)

            job.location = self.company.location

            if getattr(self, 'location_handler', None) is not None:
                r = re.compile(r'location', re.I)
                for p in d.findAll('span', attrs={'class': 'subBodytext'}):
                    m = re.search(r, p.text)
                    if m is not None:
                        t = p.findNext('div').text
                        t = unescape(t).strip()
                        l = self.location_handler(t)

                        if l:
                            job.location = l

                        break

            if not d:
                continue

            job.desc = get_all_text(d)
            job.save()
