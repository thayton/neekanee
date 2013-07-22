from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Suncor Energy',
    'hq': 'Calgary, Canada',

    'home_page_url': 'http://www.suncor.com',
    'jobs_page_url': 'https://www.suncor.apply2jobs.com/profext/index.cfm?fuseaction=mexternal.showsearchinterface',

    'empcnt': [10001]
}

class SuncorJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(SuncorJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_location_from_td(self, td):
        l = td[-3].text + ', ' + td[-2].text
        return self.parse_location(l)

def get_scraper():
    return SuncorJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
