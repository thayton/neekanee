from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'San Diego Metropolitan Transit System',
    'hq': 'San Diego, CA',

    'home_page_url': 'http://www.sdmts.com',
    'jobs_page_url': 'https://www1.apply2jobs.com/MTS/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [1001,5000]
}

class SdmtsJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(SdmtsJobScraper, self).__init__(COMPANY)

def get_scraper():
    return SdmtsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
