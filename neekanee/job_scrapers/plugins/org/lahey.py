#
# XXX The POST forms from these oracle plugins won't work unless
# you refresh the main jobs page list (or hit 'Back to results')
# every time you click on a link. Oracle seems to be maintaining
# state server-side and if you just submit the POST form "links"
# it will take you to the same job opening again and again.
#
# Solution might be to have a link that takes you to a redirection
# page. On the redirection page, you load the main jobs list page
# in a hidden iframe (as this seems sufficient to reset server state
# or get a new cookie). Then once the page has been loaded, 
# submit the job form:
#
# <script type="text/javascript">
#   function myFunc() {
#     var frm = document.getElementById("job_1");
#     frm.submit();
#   }
# </script>
#
# <iframe width="0" height="0" src="https://careers.partners.org/psc/EA/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_CE.GBL" onload="myFunc();">
# </iframe>
#
# <form name="job_1" id="job_1" method="POST" action="https://careers.partners.org/psc/EA/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_CE.GBL">
#   <input type="hidden" name="ICAction" value="POSTINGTITLE$9">
# </form>
# 
import re, urlparse, urllib, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lahey Clinic',
    'hq': 'Burlington, MA',

    'benefits': { 
        'url': 'http://www.lahey.org/About_Lahey/Careers/Employee_Benefits.aspx',
        'vacation': [] 
    },

    'home_page_url': 'http://www.lahey.org',
    'jobs_page_url': 'http://careers.lahey.org/careers',

    'empcnt': [5001,10000]
}

class LaheyJobScraper(JobScraper):
    def __init__(self):
        super(LaheyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
    
        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'contents'})
            r = re.compile(r'^jobs_list_link_\d+$')
            x = {'id': r, 'href': True}
            t = d.find('table', attrs={'class': 'info-table'})

            for a in t.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[1].text + ', MA')
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.location = l
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                jobs.append(job)
                
            try:
                self.br.follow_link(self.br.find_link(text='Next page'))
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            try:
                self.br.open(job.url)
            except:
                continue
            
            s = soupify(self.br.response().read())
            d = s.find('div', id='jobDesc')
            
            job.desc = get_all_text(d)
            job.save()
        
def get_scraper():
    return LaheyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
