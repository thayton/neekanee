from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'ExtraHop Networks',
    'hq': 'Seattle, WA',

    'contact': 'jobs@extrahop.com',

    'home_page_url': 'http://www.extrahop.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/extrahopnetworks/',

    'empcnt': [51,200]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
