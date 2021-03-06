from neekanee.jobscrapers.jobscraper import JobScraper

COMPANY = {
    'name': 'Jusin.tv',
    'hq': 'San Francisco, CA',

    'ats': 'JobVite',

    'home_page_url': 'http://www.justin.tv',
    'jobs_page_url': 'http://www.jobscore.com/jobs/twitch',

    'empcnt': [11,50]
}

class JustinTVJobScraper(JobScraper):
    def __init__(self):
        super(JustinTVJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Shut down in 2014
        self.company.job_set.all().delete()

def get_scraper():
    return JustinTVJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
