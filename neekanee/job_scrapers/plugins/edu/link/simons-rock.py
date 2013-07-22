import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bard College at Simons Rock',
    'hq': 'Great Barrington, MA',

    'home_page_url': 'http://www.simons-rock.edu',
    'jobs_page_url': 'http://www.simons-rock.edu/campus-resources/college-offices/human-resources/employment-opportunities/',

    'empcnt': [51,200]
}

class SimonsRockJobScraper(JobScraper):
    def __init__(self):
        super(SimonsRockJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'/human-resources/employment-opportunities/\S+')
        x = {'class': 'title'}

        for a in d.findAll('a', href=r):
            title = a.find('span', attrs=x)

            if not title:
                continue
            else:
                title = title.text

            if a['href'].endswith('sendto_form'):
                continue

            job = Job(company=self.company)
            job.title = title
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='portal-column-content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SimonsRockJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
