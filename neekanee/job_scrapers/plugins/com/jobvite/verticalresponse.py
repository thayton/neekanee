#################################################################
# iframe['src']=
# http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qG19Vfwv&jvresize=http://www.percussion.com/web_resources/www.percussion.com/jobvite/FrameResize.html
# 
# The jvurlargs variable used in jvGoToPage() is set within the 
# page itself and has a value such as:
#
#   ?c=qG19Vfwv&jvprefix=http%3a%2f%2fwww.percussion.com&jvresize=http%3a%2f%2fwww.percussion.com%2fweb_resources%2fwww.percussion.com%2fjobvite%2fFrameResize.html
#
# This value breaks down to:
#
#   c        = qG19Vfwv
#   jvprefix = http%3a%2f%2fwww.percussion.com
#   jvresize = http%3a%2f%2fwww.percussion.com%2fweb_resources%2fwww.percussion.com%2fjobvite%2fFrameResize.html
#
# The window.location.href value in jvGoToPage is the value of 
# the src attribute of the iframe containing the joblist.
#
#   function jvGoToPage(page, arg, jobId, argList)
#   {
#       var l = window.location.href;
#       var p = l.indexOf('?');
#
#       if (p != -1)            
#           l = l.substring(0, p); 
#       
#       l += jvurlargs + '&page=' + escape(page);
#
#       if (arg && arg.length)
#           l += '&arg=' + escape(arg);
#
#       if (jobId && jobId.length)
#           l += '&j=' + jobId;
#
#       if (argList)
#           l += argList;
#
#       window.location.href = l;
#   } 
#
# For each job jvGoToPage() is generally called with the page
# and jobId variables set as in the following example:
#
#   jvGoToPage('Job Description','','otjDVfw4')
#
# The variable 'l' gets constructed as follows as control
# passes through jvGoToPage():
#
# http://hire.jobvite.com/CompanyJobs/Careers.aspx 
#
# http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qG19Vfwv&jvprefix=http%3a%2f%2fwww.percussion.com&jvresize=http%3a%2f%2fwww.percussion.com%2fweb_resources%2fwww.percussion.com%2fjobvite%2fFrameResize.html&page=Job%20Description
#
# http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qG19Vfwv&jvprefix=http%3a%2f%2fwww.percussion.com&jvresize=http%3a%2f%2fwww.percussion.com%2fweb_resources%2fwww.percussion.com%2fjobvite%2fFrameResize.html&page=Job%20Description&j=otjDVfw4
#################################################################
import re, urllib, urlparse

from BeautifulSoup import BeautifulSoup
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'VerticalResponse',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.verticalresponse.com',
    'jobs_page_url': 'http://www.jobvite.com/CompanyJobs/Careers.aspx?c=qbY9VfwX&jvresize=/sites/www.verticalresponse.com/files/frameresize.htm',

    'empcnt': [51,200]
}

class VerticalResponseJobScraper(JobScraper):
    def __init__(self):
        super(VerticalResponseJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r"jvurlargs = '(.*)';")
        m = re.search(r, s.prettify())

        jvurlargs = m.group(1)

        d = s.find('div', attrs={'class': 'jvcontent'})
        r = re.compile(r"jvGoToPage\('(.*)','','(.*)'\)")

        for a in d.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            m = re.search(r, a['href'])
            page  = m.group(1)
            jobid = m.group(2)

            l = self.parse_location(td[-1].text)
            
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = self.mkurl(self.br.geturl(), jvurlargs, page, jobid)
            job.location = l
            jobs.append(job)

        return jobs

    def mkurl(self, url, jvurlargs, page, jobid):
        #
        # Do the same thing as jvGoToPage()
        #
        l = url[0:url.find('?')]
        l += jvurlargs + '&page=' + urllib.quote(page)
        l += '&j=' + jobid
        return l

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            a = {'class': 'jvcontent'}
            d = s.find('div', attrs=a)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return VerticalResponseJobScraper()
