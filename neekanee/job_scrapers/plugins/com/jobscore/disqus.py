from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Disqus',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.disqus.com',
    'jobs_page_url': 'http://disqus.jobscore.com/jobs/disqus/list/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
