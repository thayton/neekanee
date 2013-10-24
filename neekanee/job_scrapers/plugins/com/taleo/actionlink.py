import re, urlparse, urlutil, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ActionLink',
    'hq': 'Akron, OH',

    'ats': 'Taleo',

    'home_page_url': 'http://www.actionlink.com',
    'jobs_page_url': 'https://tbe.taleo.net/NA12/ats/careers/jobSearch.jsp?org=ACTIONLINK&cws=1',

    'empcnt': [1001,5000]
}

class ActionLinkJobScraper(JobScraper):
    def __init__(self):
        super(ActionLinkJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'requisition\.jsp\?')

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = a.text.rsplit('-', 1)

                if len(l) > 1:
                    l = l[1]
                else:
                    continue

                l = self.parse_location(l)
                if l is None:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = urlutil.url_params_del(job.url)
                job.location = l
                jobs.append(job)

            y = {'title': 'Next Page'}
            i = s.find('input', attrs=y)
            r = re.compile(r"'([^']+)")
            m = re.search(r, i['onclick'])

            tr = i.findParent('tr')
            b1 = tr.find('b', text=re.compile(r'\d+-\d+'))
            b2 = b1.findNext('b').text
            b1 = b1.split('-')[1]

            if int(b1) == int(b2):
                break

            self.br.open(m.group(1))

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('div', id='taleoContent')
            t = t.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return ActionLinkJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
