import re

from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper
from mechanize import Item

COMPANY = {
    'name': 'Chevron',
    'hq': 'San Ramon, CA',

    'home_page_url': 'http://www.chevron.com',
    'jobs_page_url': 'https://www.chevron.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [10001]
}

class ChevronJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(ChevronJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def update_frmSearch_form(self):
        """
        Limit the search to US.

        We have to select the region (North America) and then the country. However,
        the country control has its items populated dynamically when the region is
        selected. This won't work with mechanize since we can't run javascript. We
        also can't just set the country to 3 (which corresponds to the US) since 3
        doesn't show up as an option until the Javascript puts it there. Hence
        we create the item manually.

        Reference:

        http://stackoverflow.com/questions/1285895/using-python-mechanize-like-tamper-data
        """
        self.br.form.set_value_by_label(['North America'], name='searchAuxRegionID')
        item = Item(self.br.form.find_control(name='searchAuxCountryID'),
                    {'contents': '3', 'value': '3', 'label': 3})
        self.br.form['searchAuxCountryID'] = ['3']
        
    def get_location_from_desc(self, s):
        a = {'class': 'JobDetailTable'}
        t = s.find('table', attrs=a)
        r = re.compile(r'Job is available in these locations:')
        x = t.find(text=r)

        return self.parse_location(x.findNext('td').text)

def get_scraper():
    return ChevronJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
