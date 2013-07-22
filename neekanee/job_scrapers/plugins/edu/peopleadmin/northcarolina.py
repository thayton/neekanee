from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of North Carolina',
    'hq': 'Chapel Hill, NC',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.northcarolina.edu',
    'jobs_page_url': 'https://uncjobs.northcarolina.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
