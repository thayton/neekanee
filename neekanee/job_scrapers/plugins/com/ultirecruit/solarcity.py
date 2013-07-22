import re, urlparse, copy

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SolarCity',
    'hq': 'San Mateo, CA',

    'home_page_url': 'http://www.solarcity.com',
    'jobs_page_url': 'https://www11.ultirecruit.com/SOL1002/JobBoard/ListJobs.aspx',

    'empcnt': [1001,5000]
}

class SolarCityJobScraper(JobScraper):
    def __init__(self):
        super(SolarCityJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        # 
        # When we try to search for the Next page submit button
        # it breaks because the value for the button uses the
        # '>' symbol instead of the entity reference. When
        # BeautifulSoup sees the '>' it thinks it's the closing
        # tag for <input>:
        #
        #   <input type="submit" name="__Next" value=" > " 
        #
        # The fix is to replace value=" > " with value=" &gt; "
        #
        myMassage = [(re.compile(r'value=" > "'), lambda m: 'value=" &gt; "')]
        myNewMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
        myNewMassage.extend(myMassage)

        while True:
            s = BeautifulSoup(self.br.response().read(), markupMassage=myNewMassage)
            t = s.find('table', attrs={'class': 'GridTable'})
            r = re.compile(r'^JobDetails\.aspx\?__ID=')
            
            for x in t.findAll('tr'):
                td = x.findAll('td')

                if not td[0].a:
                    continue

                a = td[1].a
                if r.match(a['href']) is None:
                    continue

                l = td[2].text + ',' + td[-1].text
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            d = {'type': 'submit', 'name': '__Next', 'disabled': True}
            i = s.find('input', attrs=d)

            if i:
                break

            self.br.select_form('PXForm')
            self.br.submit(name='__Next')

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', attrs={'class': 'DetailsTable'})

            if not t:
                self.logger.debug('t is None for %s' % job.url)

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return SolarCityJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
