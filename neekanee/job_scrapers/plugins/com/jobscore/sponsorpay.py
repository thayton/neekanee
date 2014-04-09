from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'SponsorPay',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.sponsorpay.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/sponsorpay/',

    'empcnt': [51,200]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
