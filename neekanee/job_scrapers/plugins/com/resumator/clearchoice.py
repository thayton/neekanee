from neekanee.jobscrapers.resumator.resumator2 import ResumatorJobScraper

COMPANY = {
    'name': 'ClearChoice',
    'hq': 'Greenwood Village, CO',

    'home_page_url': 'http://www.clearchoice.com',
    'jobs_page_url': 'http://clearchoice.theresumator.com',

    'empcnt': [501,1000]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
