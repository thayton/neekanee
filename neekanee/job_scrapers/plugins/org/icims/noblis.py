from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Noblis',
    'hq': 'Falls Church, VA',

    'ats': 'icims',

    'home_page_url': 'http://www.noblis.org',
    'jobs_page_url': 'https://jobs-noblis.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [501,1000]
}

class NoblisJobScraper(IcimsJobScraper):
    def __init__(self):
        super(NoblisJobScraper, self).__init__(COMPANY)

def get_scraper():
    return NoblisJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
