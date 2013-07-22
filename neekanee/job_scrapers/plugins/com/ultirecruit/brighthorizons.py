import re, copy, urlparse, mechanize

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bright Horizons',
    'hq': 'Watertown, MA',

    'ats': 'ultirecruit',

    'home_page_url': 'http://www.brighthorizons.com',
    'jobs_page_url': 'https://www10.ultirecruit.com/BRI1002/JobBoard/listjobs.aspx',

    'empcnt': [10001]
}

class BrightHorizonsJobScraper(JobScraper):
    def __init__(self):
        super(BrightHorizonsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('PXForm')
#        self.br.set_all_readonly(False)
#        self.br.form['__RecordsPerPage'] = '50'
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

            for tr in t.findAll('tr'):
                td = tr.findAll('td')
                if not td[0].a:
                    continue

                a = td[0].a
                if r.match(a['href']) is None:
                    continue
                
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
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

            c = t.find('td', id='DataCell_Req_City')
            x = t.find('td', id='DataCell_Req_State')
            l = self.parse_location(c.text + ',' + x.text)
            
            if not l:
                continue

            job.location = l
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return BrightHorizonsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
