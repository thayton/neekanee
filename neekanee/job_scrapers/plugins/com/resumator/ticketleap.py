from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Ticket Leap',
    'hq': 'Philadelphia, PA',

    'home_page_url': 'http://www.ticketleap.com',
    'jobs_page_url': 'http://ticketleap.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
