import sys
import json

from models import *
from pysolr import Results, Solr
from urlparse import urlparse, parse_qs, ParseResult
from django.core.exceptions import ObjectDoesNotExist

def load_jobs_file(jobs_file, add_to_solr=False):
    """
    Load JSON encoded jobs file. The param jobs_file is an 
    instance of UploadedFile with jobs in JSON format
    """

    #
    # Get existing company object or create a new one based
    # off of contents of file. Then delete existing jobs for
    # this company from dbase to make way for new jobs.
    #
    c = json.loads(jobs_file.read())
    company = deserialize_company_dict(c)

    #
    # Remove all jobs for this company from SOLR. All the jobs for this company
    # will get reindexed into SOLR so we can capture any changes to the company
    # profile (since the last indexing) into the SOLR job document.
    #
    if add_to_solr:
        delete_docs(q='company_id:%d' % company.id)

    #
    # Just to be safe ensure that the md5 checksums for the jobs currently
    # in the database for this company are set
    #
    for job in company.job_set.all():
        if len(job.md5) == 0:
            job.md5 = job.hexdigest()
            job.save()

    #
    # We identify jobs by the md5 checksums to determine which jobs are
    # new and need to be added, and which jobs currently in the database
    # are no longer listed and need to be deleted
    #
    # jobs_to_add = listed_jobs_checksums - stored_jobs_checksums
    # jobs_to_del = stored_jobs_checksums - listed_jobs_checksums
    #
    listed_jobs = [ deserialize_job_dict(company, j) for j in c['jobs'] ]
    listed_jobs_checksums = set([ '%s' % j.md5 for j in listed_jobs ])
    stored_jobs_checksums = set([ '%s' % j.md5 for j in company.job_set.all()])

    jobs_to_delete = stored_jobs_checksums - listed_jobs_checksums

    for cksum in jobs_to_delete:
        job = company.job_set.get(md5=cksum)
        job.delete()

    jobs_to_add = listed_jobs_checksums - stored_jobs_checksums
    jobs_added_successfully = []

    for job in listed_jobs:
        if job.md5 in jobs_to_add:
            #
            # Sanity check - delete any existing jobs with this checksum
            # This should have been caught above in the job_to_delete loop
            # but is here as precaution
            #
            Job.objects.filter(md5=job.md5).delete()

            try:
                job.save()
            except _mysql_exceptions.Warning, e:
                print "job.save() generated an exception: %s" % e
            else:
                print "job added successfully"
                jobs_added_successfully.append(job.id)

    # 
    # If the job.save() call above fails, we end up in a weird state
    # where job.id is not set. Because it's not set, we can't call
    # job.delete() to remove the job. But we can see the job in
    # company.job_set.all() with its id set there. 
    #
    # We want to remove the offending job and the only way seems to 
    # be to track which jobs were added succesfully and remove any 
    # jobs whose id doesn't show up in this list
    #
    for job in company.job_set.all():
        if job.md5 in jobs_to_add and job.id not in jobs_added_successfully:
            job.delete()

    if add_to_solr:
        index_jobs_for_company(company)

def index_jobs_for_company(company):
    """
    Add all of a companies jobs to the SOLR index.
    """
    docs = []
    for job in company.job_set.all():
        solr_doc = denormalize_job_to_solr_doc(job)
        docs.append(solr_doc)

    add_doc(json.dumps(docs))
    commit()
    
def denormalize_job_to_solr_doc(job):
    """
    Denormalize Job object into a format suitable for addition to SOLR.
    The SOLR schema.xml file defines the document schema.
    """
    doc = {}
    doc['id'] = job.id
    doc['title'] = job.title
    doc['desc'] = job.desc
    doc['url'] = job.url
    doc['url_data'] = job.url_data
    doc['company_id'] = job.company.id
    doc['company_name'] = job.company.name
    doc['company_ats'] = job.company.ats
    doc['company_jobs_page_url'] = job.company.jobs_page_url
    doc['tld'] = job.company.tld
    doc['city'] = job.location.city
    doc['state'] = job.location.state
    doc['country'] = job.location.country
    doc['latlng'] = '%f,%f' % (job.location.lat,job.location.lng)

    if job.company.empcnt:
        doc['company_size'] = job.company.empcnt.id

    if job.company.companytag_set.count() > 0:
        doc['company_tags'] = [ '%s' % x.tag.name for x in job.company.companytag_set.all() ]

    if job.company.companyaward_set.count() > 0:
        doc['company_awards'] = [ '%d' % x.award.pk for x in job.company.companyaward_set.all() ]

    if job.company.vacationaccrual_set.filter(year=1).count() == 1:
        doc['vacation_year_1'] = int(job.company.vacationaccrual_set.get(year=1).days)

    # If the company has location specific tags then we set those for the
    # SOLR job document
    try:
        company_location = job.company.companylocation_set.get(location=job.location)
    except ObjectDoesNotExist:
        pass
    else:
        if company_location.companylocationtag_set.all().count() > 0:
            doc['company_location_tags'] = [ '%s' % x.tag.name for x in company_location.companylocationtag_set.all() ]

    return doc

def deserialize_company_dict(c):
    """
    Create (or load) a Company() object from company/jobs dictionary
    """
    l = deserialize_location_dict(c['hq'])
    try:
        company = Company.objects.get(home_page_url=c['home_page_url'])
    except ObjectDoesNotExist:
        company = Company()

    company.name = c['name']
    company.home_page_url = c['home_page_url']
    company.jobs_page_url = c['jobs_page_url']
    company.location = l

    netloc = urlparse(company.home_page_url).netloc
    company.tld = netloc.rsplit('.', 1)[1]

    if c.has_key('empcnt'):
        try:
            if len(c['empcnt']) == 1:
                company_size = CompanySize.objects.get(lo=c['empcnt'][0])
            else:
                company_size = CompanySize.objects.get(lo=c['empcnt'][0], hi=c['empcnt'][1])

            company.empcnt = company_size
        except ObjectDoesNotExist:
            print "error: invalid company size", c['empcnt']
            raise

    if c.has_key('ats'):
        company.ats = c['ats']

    company.save()

    return company

def deserialize_job_dict(company, j):
    """
    Create a new Job() object for company given jobs data dictionary j
    """
    job = Job()

    try:
        job.title = j['title']
        job.url = j['url']
        job.url_data = j.has_key('url_data') and j['url_data'] or ''
        job.desc = j['desc']
        job.company = company
    except KeyError as e:
        print "KeyError for %s: %s" % (company.name, e)
        return None

    if j.has_key('location') and j['location'] is not None:
        l = deserialize_location_dict(j['location'])
    else:
        l = company.location

    job.location = l
    job.company = company
    job.md5 = job.hexdigest()

    return job

def deserialize_location_dict(l):
    """
    Create a new Location() object given location dictionary
    """
    if l['country'] == 'us' and len(l['state']) != 2:
        sys.stderr.write('Warning- state more than two chars long: %s\n' % l['state'])

    try:
        if l['country'] == 'us':
            loc = Location.objects.get(city=l['city'], 
                                       state=l['state'],
                                       country=l['country'])
        else:
            loc = Location.objects.get(city=l['city'], 
                                       country=l['country'])

    except ObjectDoesNotExist:
        print 'location %s does not exist' % l
        if l['country'] == 'us':
            loc = Location(city=l['city'], 
                           state=l['state'],
                           country=l['country'])
        else:
            loc = Location(city=l['city'], 
                           country=l['country'])

        loc.lat = l['coord'][0]
        loc.lng = l['coord'][1]
        loc.save()    

    return loc
