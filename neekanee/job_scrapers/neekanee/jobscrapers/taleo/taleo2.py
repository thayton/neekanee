import re, urlparse, urlutil

from ghost import Ghost
from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

class TaleoJobScraper(JobScraper):
    def __init__(self, company_dict):
        super(TaleoJobScraper, self).__init__(company_dict)
        self.ghost = Ghost()

    def scrape_job_links(self, url):
        jobs = []

        self.ghost.open(url)
        self.ghost.wait_for_page_loaded()

        pageno = 2

        while True:
            s = BeautifulSoup(self.ghost.content)

            for id in s.findAll(text='Requisition ID'):
                td = id.findParent('td')

                x = {'class': 'morelocation'}
                l = td.find('div', attrs=x)
                l = self.parse_location(l.text)

                if not l:
                    continue

                x = {'class': 'titlelink'}
                t = td.find('span', attrs=x)

                job = Job(company=self.company)
                job.title = t.text
                job.location = l

                d = id.findParent('div')
                x = d.findAll('span')
                q = 'jobdetail.ftl?job=' + x[-1].text + '&lang=en'

                job.url = urlparse.urljoin(url, q)
                jobs.append(job)

            a = s.find(title='Go to the next page')
            selector = a['id'].replace('.', '\.')

            result,_ = self.ghost.evaluate(
                "document.getElementById('%s').parentNode.getAttribute('class');" % selector)

            r = re.compile(r'Page (\d+) out of (\d+)')
            t = s.find(text=r)

            if t:
                m = re.search(r, t)
                p1,p2 = m.group(1),m.group(2)
                if p1 == p2:
                    break

            result,_ = self.ghost.evaluate(
                """
                var element = document.querySelector('%s'); 
                var evt = document.createEvent('MouseEvents'); 
                evt.initMouseEvent("click", true, true, window, 1, 1, 1, 1, 1, false, false, false, false, 0, element);
                document.getElementById('%s').onclick(evt);
                """ % (selector, selector), expect_loading=True)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.ghost.open(job.url)
            self.ghost.wait_for_page_loaded()

            s = soupify(self.ghost.content)
            d = s.find('div', id='requisitionDescriptionInterface.descRequisitionContainer')

            job.desc = get_all_text(d)
            job.save()


