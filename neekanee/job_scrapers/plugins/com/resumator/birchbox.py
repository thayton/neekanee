from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Birch Box',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.birchbox.com',
    'jobs_page_url': 'http://birchbox.theresumator.com',

    'empcnt': [201,500]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
