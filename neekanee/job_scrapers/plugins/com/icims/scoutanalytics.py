from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'ScoutAnalytics',
    'hq': 'Issaquah, WA',

    'home_page_url': 'http://scoutanalytics.com',
    'jobs_page_url': 'https://careers-servicesource.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [11,50]
}

class ScoutAnalyticsJobScraper(IcimsJobScraper):
    def __init__(self):
        super(ScoutAnalyticsJobScraper, self).__init__(COMPANY)


def get_scraper():
    return ScoutAnalyticsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
