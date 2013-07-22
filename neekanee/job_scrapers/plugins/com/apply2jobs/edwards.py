from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Edwards',
    'hq': 'Irvine, CA',

    'home_page_url': 'http://www.edwards.com',
    'jobs_page_url': 'https://www.edwards.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [5001, 10000]
}

class EdwardsJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(EdwardsJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_location_from_td(self, td):
        l = td[-3].text + ', ' + td[-1].text
        return self.parse_location(l)

def get_scraper():
    return EdwardsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
