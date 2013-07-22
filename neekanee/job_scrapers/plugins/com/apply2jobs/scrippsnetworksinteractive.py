from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Scripps Networks Interactive',
    'hq': 'Knoxville, TN',

    'home_page_url': 'http://www.scrippsnetworksinteractive.com',
    'jobs_page_url': 'https://www2.apply2jobs.com/scrippsnetworksinteractive/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [1001,5000]
}

class ScrippsNetworksInteractiveJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(ScrippsNetworksInteractiveJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = '-'.join(['%s' % x.text for x in td[-3:]])
        return self.parse_location(l)

def get_scraper():
    return ScrippsNetworksInteractiveJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
