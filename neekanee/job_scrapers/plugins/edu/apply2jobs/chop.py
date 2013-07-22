from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Children\'s Hospital of Philadelphia',
    'hq': 'Philadelphia, PA',

    'home_page_url': 'http://www.chop.edu',
    'jobs_page_url': 'https://www.chop.edu.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [10001]
}

class ChopJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(ChopJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

def get_scraper():
    return ChopJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
