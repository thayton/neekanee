import re, copy, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from BeautifulSoup import BeautifulSoup

from neekanee_solr.models import *

COMPANY = {
    'name': 'Resolute Energy Corporation',
    'hq': 'Denver, CO',

    'ats': 'UltiRecruit',

    'home_page_url': 'http://www.resolutenaturalresources.com',
    'jobs_page_url': 'https://rew11.ultipro.com/RES1008/JobBoard/SearchJobs.aspx?Page=Search',

    'empcnt': [51,200]
}

class ResoluteNaturalResourcesJobScraper(JobScraper):
    def __init__(self):
        super(ResoluteNaturalResourcesJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('PXForm')
        self.br.form['RecordsPerPage'] = ['50']
        self.br.submit()

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

                a = td[2].a
                if r.match(a['href']) is None:
                    continue
                
                l = self.parse_location(td[-2].text + ',' + td[-1].text)
                if l is None:
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

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return ResoluteNaturalResourcesJobScraper()
        
if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
