import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

class PeopleAdminJobScraper(JobScraper):
    def __init__(self, company_dict):
        company_dict['ats']= 'PeopleAdmin'
        super(PeopleAdminJobScraper, self).__init__(company_dict)

    def select_jobSearch_form(self):
        """
        Derived classes should override in order to set any controls in
        hrSearch form prior to submitting the form. Form will already be
        selected when this method is invoked.
        """
        pass

    def update_jobSearch_form(self):
        """
        Derived classes should override in order to set any controls in
        hrSearch form prior to submitting the form. Form will already be
        selected when this method is invoked.
        """
        pass

    def submit_jobSearch_form(self):
        """
        Derived classes should override in order to set any controls in
        hrSearch form prior to submitting the form. Form will already be
        selected when this method is invoked.
        """
        pass

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text='Search Jobs'))
        self.select_jobSearch_form()
        self.update_jobSearch_form()
        self.submit_jobSearch_form()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='search_results')

            for t in d.findAll('td', attrs={'class': 'job-title'}):
                job = Job(company=self.company)
                job.title = t.a.text
                job.url = urlparse.urljoin(self.br.geturl(), t.a['href'])
                job.location = self.company.location
                jobs.append(job)

            # Navigate to the next page
            try:
                r = re.compile(r'^%d$' % pageno)
                n = self.br.find_link(text_regex=r)
                self.br.follow_link(n)
            except mechanize.LinkNotFoundError:
                break
            else:
                pageno += 1

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content_inner')

            if getattr(self, 'location_handler', None) is not None:
                t = d.find(text='Campus Location: ')
                if t is not None:
                    t = t.parent.findNext('td').text
                    l = self.location_handler(t)
                    if l:
                        job.location = l

            job.desc = get_all_text(d)
            job.save()
