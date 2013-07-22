import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Riverbed Tecnologies',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.riverbed.com',
    'jobs_page_url': 'http://recruit.trovix.com/jobhostmaster/jobhost/ListJobPosts.do?accountId=147a1477488137d390a50032705dd8f4b4dafcb9&action=listJobPosts&refresh=1',

    'empcnt': [1001,5000]
}

class RiverbedJobScraper(JobScraper):
    def __init__(self):
        super(RiverbedJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('ListJobPostsForm')
        self.br.submit()

        pageno = 2
        r = re.compile(r'^ViewJobPostDetails\.do\?')

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[-2].text)
                if l is None:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            try:
                x = re.compile(r'/jobhostmaster/jobhost/ListJobPosts\.do\?.*&p=%d&' % pageno)
                pageno += 1
                self.br.follow_link(self.br.find_link(url_regex=x))
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
            f = s.find('form', attrs={'name': 'ViewJobPostDetailsForm'})

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return RiverbedJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
