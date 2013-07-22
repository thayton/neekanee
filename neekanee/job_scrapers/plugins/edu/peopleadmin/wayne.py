from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Wayne State University',
    'hq': 'Detroit, MI',

    'home_page_url': 'http://www.wayne.edu',
    'jobs_page_url': 'https://jobs.wayne.edu/applicants/jsp/shared/Welcome_css.jsp',

    'gctw_chronicle': True,

    'empcnt': [5001,10000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
