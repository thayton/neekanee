import urlparse

from ghost import Ghost
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
        d = id.findParent('div')
        x = d.findAll('span')
        q = 'jobdetail.ftl?job=' + x[-1].text + '&lang=en'
        u = urlparse.urljoin(url, q)
        jobs.append(u)
        print u

      a = s.find(title='Go to the next page')
      selector = a['id'].replace('.', '\.')

      result,_ = self.ghost.evaluate(
        "document.getElementById('%s').parentNode.getAttribute('class');" % selector)

      if result == 'pagerlinkoff':
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
    new_jobs = self.scrape_job_links(url)
    print '# jobs: ', len(new_jobs)

    for job_url in new_jobs:
      self.ghost.open(job_url)
      self.ghost.wait_for_page_loaded()

      s = BeautifulSoup(self.ghost.content)
      d = s.find('div', id='requisitionDescriptionInterface.descRequisitionContainer')

      print d.text

if __name__ == '__main__':
  job_scraper = TaleoJobScraper()
  job_scraper.scrape_jobs()
