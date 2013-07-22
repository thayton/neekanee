from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'EOG Resources',
    'hq': 'Houston, Texas',

    'home_page_url': 'http://www.eogresources.com',
    'jobs_page_url': 'https://www1.apply2jobs.com/EOGResources/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [1001, 5000]
}

class EogResourcesJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(EogResourcesJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = ', '.join(['%s' % x.text for x in td[3:6]])
        return self.parse_location(l)

def get_scraper():
    return EogResourcesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
