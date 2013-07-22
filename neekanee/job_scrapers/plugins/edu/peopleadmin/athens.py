from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Athens State University',
    'hq': 'Athens, AL',

    'home_page_url': 'http://www.athens.edu',
    'jobs_page_url': 'https://jobs.athens.edu',

    'empcnt': [201,500]
}


def get_scraper():
    job_scraper = PeopleAdminJobScraper(COMPANY)
    job_scraper.link_text = 'Search Jobs'
    return job_scraper

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
                            
