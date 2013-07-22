import os
import re
import sys
import json
import math
import json
import urllib
import urllib2
import random
import _mysql_exceptions 

from linkup import LinkUp, LinkUpResults
from models import *
from forms import *
from urlparse import urlparse, parse_qs, ParseResult
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.template.defaultfilters import slugify
from geopy import geocoders
from urllib import quote_plus
from pysolr import Results, Solr
from solr_query_builder import *
from job_categories import job_categories, job_category_titles
from job_titles import job_titles
from templatetags.neek_extras import state_abbrev_to_name, country_abbrev_to_name

def user_display(user):
    '''
    Callable for user_display in templates
    '''
    if user.first_name and user.last_name:
        return user.get_full_name()
    else:
        return user.username

@login_required
def user_profile(request):
    """ 
    Render form displaying user stats 
    """
    vars = RequestContext(request)
    return render_to_response('account/profile.html', vars)

@login_required
def user_job_alerts(request):
    """ 
    Render form displaying user stats 
    """
    vars = RequestContext(request)
    return render_to_response('account/job_alerts.html', vars)

@login_required
def user_job_basket(request):
    """ 
    Render form displaying user stats 
    """
    vars = RequestContext(request)
    return render_to_response('account/job_basket.html', vars)

@login_required
def create_job_alert(request, query):
    alert = JobAlert()
    alert.query = query
    alert.user = request.user
    alert.save()
    return HttpResponseRedirect('/account/job_alerts/')

@login_required
def delete_job_alert(request, alert_id):
    try:
        alert = request.user.jobalert_set.get(pk=alert_id)
    except JobAlert.DoesNotExist:
        raise Http404
    else:
        alert.delete()
        return HttpResponseRedirect('/account/job_alerts/')

def delete_job_alert_from_email(request, alert_key):
    """
    This view handles the case where the user clicks on the 
    'Delete this job alert' link from a job alert email they've
    received.
    """
    try:
        alert = JobAlert.objects.get(key=alert_key)
    except JobAlert.DoesNotExist:
        raise Http404
    else:
        alert.delete()
        vars = RequestContext(request)
        return render_to_response('account/job_alert_deleted.html', vars)
    
@login_required
def edit_job_alert(request, alert_id):
    try:
        alert = request.user.jobalert_set.get(pk=alert_id)
    except JobAlert.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        form = JobAlertForm(request.POST, instance=alert)
        if form.is_valid():
            form.save()

    return HttpResponseRedirect('/account/job_alerts/')

@login_required
def add_job_to_basket(request, job_id):
    #
    # Don't add the job if it's alread been bookmarked by this user
    #
    job = get_object_or_404(Job, pk=job_id)
    try:
        bookmark = request.user.jobbookmark_set.get(job=job)
    except JobBookmark.DoesNotExist:
        pass
    else:
        return HttpResponseRedirect('/account/job_basket/')

    bookmark = JobBookmark()
    bookmark.job = job
    bookmark.user = request.user
    bookmark.save()

    return HttpResponseRedirect('/account/job_basket/')

@login_required
def delete_job_from_basket(request, bookmark_id):
    try:
        bookmark = request.user.jobbookmark_set.get(pk=bookmark_id)
    except JobBookmark.DoesNotExist:
        raise Http404
    else:
        bookmark.delete()
        return HttpResponseRedirect('/account/job_basket/')

@login_required
def logout_page(request):
    """ 
    Handle logout and redirect to main page 
    """
    logout(request)
    return HttpResponseRedirect('/')

def register_page(request):
    """ 
    Display user account registration form or if request.method == POST 
    then user has just submitted the form in which case we validate and 
    process the form
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
            
    vars = RequestContext(request, { 'form': form })
    return render_to_response('registration/register.html', vars)

#
# XXX Make this class look like a list of numFound objects
# and have it be sliceable so we can use it directly with paginator
#
class SearchResults(Results):
    """
    Extension of pysolr Results class that sorts and zips some of the facet
    fields.
    """
    def __init__(self, results):
        Results.__init__(self, **results.__dict__)
        self.cookie_stuffing_urls = []
        self.hits = int(self.hits)

        self.facet_ranges_to_facet_fields()
        self.zip_facet_fields()
        self.sort_facet_fields()
        self.highlight_desc()
        self.set_companies()

    def facet_ranges_to_facet_fields(self):
        """
        For now this just moves the facet counts for the vacation_year_1 range
        into the facet_fields{} so we can handle it the same way we do facet_fields.

        "facet_ranges":{
          "vacation_year_1":{
            "counts":[...]
        """
        if self.facets.has_key('facet_ranges') and self.facets['facet_ranges'].has_key('vacation_year_1'):
            counts = self.facets['facet_ranges']['vacation_year_1']['counts']
            self.facets['facet_fields']['vacation_year_1'] = counts

    def highlight_desc(self):
        """ Put highlight results into docs['highlight'] field """
        if self.highlighting:
            for doc in self.docs:
                doc['highlight'] = ''.join(self.highlighting[doc['id']]['desc']) + '...'

    def set_companies(self):
        """ 
        XXX We still need company reference to get at company rating 
        and reviews.
        """
        for doc in self.docs:
            if doc.has_key('company_id'):
                company = Company.objects.get(pk=doc['company_id'])
                doc['company'] = company

                #
                # Sites using Kenexa/BrassRing ATS require cookie-stuffing to 
                # get the links to load. Make a list of the company jobs page
                # URLs using Kenexa/Brassring so the cookie-stuffing can be
                # done on the front-end
                #
                ats = company.ats.lower()
                if ats == 'kenexa' or ats == 'brassring':
                    if company.jobs_page_url not in self.cookie_stuffing_urls:
                        self.cookie_stuffing_urls.append(company.jobs_page_url)

    def zip_facet_fields(self):
        """
        Tupalize the results of the facet counts so we can access the results
        as pairs in the templates. 

          facet_fields.title = [ "game",6, "designer",5, "yoga",1] 

        becomes

          facet_fields.title = [ ("game",6), ("designer",5), ("yoga",1)] 

        In the templates, we can then access these values as:

          for title,count in facet_fields.title:
            {{ title }}, {{ count }}
            ...
        """    
        if self.facets.has_key('facet_fields'):
            for field,counts in self.facets['facet_fields'].items():
                zipped = zip(counts[0::2], counts[1::2])
                self.facets['facet_fields'][field] = zipped

    def sort_facet_fields(self):
        """
        The default ordering for the facet counts may be overridden by
        defining a sort_<field>_facet method in this class. This function
        calls all such methods.
        """
        if self.facets.has_key('facet_fields'):
            for field in self.facets['facet_fields'].keys():
                func = getattr(self, 'sort_%s_facet' % field, None)
                if callable(func):
                    func()

    def sort_vacation_year_1_facet(self):
        """
        Sort the results for vacation_year_1 in ascending order based
        on the number of days. 
        """
        field = self.facets['facet_fields']['vacation_year_1']
        field.sort(key=lambda x: x[0])

    def sort_company_size_facet(self):
        """
        Sort the results for company_size in ascending order based
        on the primary key. This way the results show up ordered by
        smallest company to largest company.
        """
        field = self.facets['facet_fields']['company_size']
        field.sort(key=lambda x: x[0])

KM_PER_MILE = 1.61

def index(request):
    return render_to_response('index.html', RequestContext(request))

def latlng_context(results):
    """
    Set the lat,lng for each location in the results. This will be used
    by the map drawing code in the templates to plot where the jobs are.

    The result returned is a dictionary keyed on either cities, states,
    or countries, where each keys value is the associated lat,lng.
    """
    context = {}

    if len(results.facets['facet_fields']['country']) > 1:
        for country,cnt in results.facets['facet_fields']['country']:
            try:
                l = Location.objects.get(city='', state='', country=country)
            except ObjectDoesNotExist:
                continue
            else:
                context[country] = ('%f' % l.lat, '%f' % l.lng)
    elif len(results.facets['facet_fields']['state']) > 1:
        for state,cnt in results.facets['facet_fields']['state']:
            try:
                l = Location.objects.get(city='', state=state, country='us')
            except ObjectDoesNotExist:
                continue
            else:
                context[state] = ('%f' % l.lat, '%f' % l.lng)
    elif len(results.facets['facet_fields']['country']) > 0:
        country,_ = results.facets['facet_fields']['country'][0]

        if len(results.facets['facet_fields']['state']) == 1:
            state,_ = results.facets['facet_fields']['state'][0]
        else:
            state = ''
            
        for city,cnt in results.facets['facet_fields']['city']:
            try:
                l = Location.objects.get(city=city, state=state, country=country)
            except ObjectDoesNotExist:
                continue
            else:
                context[city] = ('%f' % l.lat, '%f' % l.lng)

    return { 'latlng': context }

def active_filters_context(get):
    """
    Return a list of links that allow the user to remove
    a search filter by clicking on the link. For example, 
    the url below contains three filters (rating, awards, 
    and size):

      http://127.0.0.1:8000/jobs/?rating=3&award=1&size=1

    To remove the rating filter, we provide the link:

      http://127.0.0.1:8000/jobs/?awards=1&size=1

    To remove the award filter, we provide the link:

      http://127.0.0.1:8000/jobs/?rating=3&size=1

    To remove the size filter, we provide the link:

      http://127.0.0.1:8000/jobs/?rating=3&awards=1
    """
    context = {}
    filters = [
        'tld', 'company', 'size', 'title', 'country', 'state', 'city'
    ]

    for filter in filters:
        if get.has_key(filter):
            GET = get.copy()
            del GET[filter]

            if filter == 'country':
                if 'state' in GET: 
                    del GET['state']
                if 'city' in GET:
                    del GET['city']

            if filter == 'state':
                if 'city' in GET:
                    del GET['city']

            context[filter] = GET.urlencode()
            print 'context=', context

    return {'remove_filter': context}

def search(request):
    """ 
    Submitting a search from index.html goes to /search where 
    we redirect the query based on the search parameters.
    """
    get = request.GET.copy()
    print get

    for k in get.keys():
        if len(get[k]) == 0:
            del get[k]

    # Client should lookup location via javascript but if they
    # don't lat,lng won't be in URL and we have to do it here.
    if not get.has_key('lat') and get.has_key('loc'):
        geocoder = geocoders.Google()
        try:
            results = geocoder.geocode(get['loc'], exactly_one=False)
            _, (lat,lng) = results[0]
            get['lat'] = '%.2f' % float(lat)
            get['lng'] = '%.2f' % float(lng)

            if not get.has_key('radius'):
                get['radius'] = 25
        except:
            del get['loc']            
            if get.has_key('radius'):
                del get['radius']
    elif not get.has_key('lat') and not get.has_key('lng'):
        if get.has_key('radius'):
            del get['radius']

    return HttpResponseRedirect('/jobs/?%s' % get.urlencode())

def browse_jobs(request):
    vars = RequestContext(request)
    vars.update({'job_categories': job_categories})
    vars.update({'company_tags': Tag.objects.all()})
    vars.update({'company_tlds': Company.objects.all().values_list('tld', flat=True).distinct()})
    vars.update({'company_sizes': CompanySize.objects.all()})
    return render_to_response('jobs/browse_jobs.html', vars)

def browse_jobs_by_category(request, category):
    vars = RequestContext(request)
    vars.update({'category': category})
    vars.update({'job_titles': job_category_titles[category]})
    return render_to_response('jobs/browse_job_category.html', vars)

def browse_jobs_by_company(request, name):
    vars = RequestContext(request)
    vars.update({'name_startswith': name})
    vars.update({'companies': Company.objects.filter(name__istartswith=name)})
    return render_to_response('jobs/browse_jobs_by_company.html', vars)

def browse_jobs_by_job_title(request, title):
    vars = RequestContext(request)
    vars.update({'title_startswith': title})
    vars.update({'job_titles': job_titles[title]})
    return render_to_response('jobs/browse_jobs_by_job_title.html', vars)

def filter_companies(request):
    """
    Handle query parameters for /companies/ 
    """
    #
    # ~Q matches everything
    #
    q = Q()

    if request.GET.get('tld', None):
        q = (q & Q(tld=request.GET['tld']))

    if request.GET.get('size', None):
        q = (q & Q(empcnt=request.GET['size']))

    if request.GET.get('name', None):
        q = (q & Q(name__icontains=request.GET['name']))

    if request.GET.get('vacation', None):
        days = int(request.GET['vacation'])
        q = (q & Q(vacationaccrual__year__exact=1) & \
                 Q(vacationaccrual__days__gte=days) & \
                 Q(vacationaccrual__days__lt=days + 5))

    query_set = Company.objects.filter(q)

    #
    # The following filters are complex because we have to match on multiple values. So 
    # if we're filtering on tags #highered and #education that Count(companytag) should
    # be equal to 2.
    #
    # Reference: 
    # http://stackoverflow.com/questions/10067171/check-for-multiple-values-in-a-m2m-relationship-in-django
    #
    if request.GET.get('tags', None):
        tags = request.GET.get('tags').split()
        for tag in tags:
            query_set = query_set.filter(companytag__tag__name__in=[tag])

    if request.GET.get('awards', None):
        awards = request.GET.get('awards').split()
        for award in awards:
            query_set = query_set.filter(companyaward__award__id__in=[award]).distinct()

    return query_set

def companies_facet_counts(query_set):
    """
    Generate facet counts for /companies/
    """
    qs_company_pks = query_set.values_list('pk', flat=True)
    companies_in_qs = Company.objects.filter(id__in=qs_company_pks)

    tld = []
    for item in companies_in_qs.values('tld').annotate(Count('id')).order_by('-id__count'):
        tld.extend([ ('%s' % item['tld'], '%d' % item['id__count']) ])

    size = []
    for item in companies_in_qs.values('empcnt').annotate(Count('id')).order_by('empcnt'):
        size.extend([ ('%s' % item['empcnt'], '%d' % item['id__count']) ])

    tags = []
    for item in CompanyTag.objects.filter(company__in=qs_company_pks).values('tag__name').annotate(Count('id')).order_by('-id__count'):
        if item['tag__name']:
            tags.extend([ ('%s' % item['tag__name'], '%d' % item['id__count']) ])

    #
    # Trying to achieve this:
    # mysql> select award_id,count(distinct company_id, award_id) from neekanee_solr_companyaward group by award_id;
    #
    awards = {}
    for item in CompanyAward.objects.filter(company__in=qs_company_pks).values('company_id', 'award_id').distinct():
        awards['%d' % item['award_id']] = awards.get('%d' % item['award_id'], 0) + 1

    awards = awards.items()

    # Vacation is measured in 5 day gaps (10-14 days vacation, 15-19 days vacation, etc.)
    vacation = { 10:0, 15:0, 20:0, 25:0, 30:0 }

    for item in companies_in_qs.filter(vacationaccrual__year__exact=1).values('vacationaccrual__days').annotate(Count('id')):
        if item['vacationaccrual__days']:
            for days in vacation.keys():
                if item['vacationaccrual__days'] >= days and item['vacationaccrual__days'] < days + 5:
                    vacation[days] += item['id__count']
                    break

    vacation = vacation.items()
    vacation.sort(key=lambda x: x[0])

    return { 'facet_counts': 
             { 'tld': tld, 'company_size': size, 'company_tags': tags, 'company_awards': awards, 'vacation_year_1': vacation }}


def companies(request):
    """ 
    List companies along with the number of employee reviews for each company
    """
    query_set = filter_companies(request)
    facets = companies_facet_counts(query_set)

    page_vars = paginate(query_set, request.GET, 'companies')

    vars = RequestContext(request)
    vars.update(page_vars)
    vars.update(facets)

    return render_to_response('companies/companies.html', vars)

def company(request, **args):
    """ 
    Return the details page for a company. This page includes company stats, photos, 
    reviews, etc. 
    """
    if args.has_key('cid'):
        company = get_object_or_404(Company, pk=args['cid'])
    else:
        company = get_object_or_404(Company, name_slug=args['cslug'])

    vars = RequestContext(request, { 'company': company })

    return render_to_response('companies/company.html', vars)

@login_required
def job_alerts(request):
    job_alert = request.user.jobalert_set.all()[0]

    from django.http import QueryDict    

    query_builder = SOLRJobSearchQueryBuilder(10)
    query = query_builder.build_query(QueryDict(job_alert.query))

    conn = Solr('http://127.0.0.1:8983/solr/')
    results = SearchResults(conn.search(**query))

    vars = RequestContext(request, { 'jobs': results.docs })
    return render_to_response('account/job_alerts_email.html', vars)

def job(request, jobid):
    job = get_object_or_404(Job, pk=jobid)

def isrobot(request):
    bots = ['googlebot', 'yandex', 'baidu', 'bing', 'robot', 'spider']
    user_agent = request.META.get('HTTP_USER_AGENT')

    if user_agent is None:
        return False

    user_agent = user_agent.lower()
    for bot in bots:
        if user_agent.find(bot) != -1:
            return True
    
    return False

def get_client_ip(request):
    '''
    Return the IP address of the client that connected to us
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def broken_miami_edu_links(request, **args):
    url = re.sub(r'-universiy-', '-university-',  request.path)
    return HttpResponseRedirect(url)

def broken_bbt_links(request, **args):
    url = re.sub(r'-bb$',    '-bbt',  request.path)
    url = re.sub(r'-bb-',    '-bbt-', url)
    url = re.sub(r'-bb26t$', '-bbt',  url)
    url = re.sub(r'-bb26t-', '-bbt-', url)
    return HttpResponseRedirect(url)

def broken_city_links(request, **args):
    ''' Fix broken links where only the city is specified '''
    r = re.compile(r'-in-(.*)$')
    m = re.search(r, request.path)
    l = Location.objects.filter(slug__startswith=m.group(1))

    if len(l) == 0:
        raise Http404
    else:
        l = l[0]

    url = re.sub(r'%s$' % m.group(1), l.slug, request.path, count=1)
    return HttpResponseRedirect(url)

def broken_states_links(request, **args):
    return HttpResponseRedirect('%sus' % request.path)

def seosearch(request, **args):
    '''
    XXX TODO
    This duplicates most of the code in jobs() below
    '''
    get = request.GET.copy()
    get.update(args)

    request.path = '/jobs/'

    if get.has_key('q'):
        get['q'] = get['q'].replace('-', ' ')

    if get.has_key('city'):
        get['city'] = get['city'].replace('-', ' ')

    if get.has_key('cslug'):
        company = get_object_or_404(Company, name_slug=get['cslug'])
        del (get['cslug'])
        get['company'] = company.name

    # Ensure the location actually exists
    l = ' '.join([get.get('city', ''), get.get('state', ''), get.get('country', '')])
    if get.get('city', None):
        slug = slugify(l)
        try:
            # XXX
            # Sometimes multiple locations will have the same slug because of 
            # special characters. Should fix this
            Location.objects.filter(slug=slug)
        except Location.DoesNotExist:
            raise Http404

    # Fill in location field of search box  
    if get.get('state', None):
        if not get.get('city', None):
            get['loc'] = state_abbrev_to_name(get.get('state'))
        else:
            get['loc'] = get.get('city').title() + ', ' + get.get('state').upper()
    elif get.get('country', None):
        if not get.get('city', None):
            get['loc'] = country_abbrev_to_name(get.get('country')).title()
        else:
            get['loc'] = get.get('city').title() + ', ' + country_abbrev_to_name(get.get('country')).title()

    # XXX
    # Note that you could remove city,state,country filters here and do a regular
    # radius search so that results would show up for all locations within a 25-mile
    # radius of the search location, which might look better in Google than 0-results
    # pages.
    #
    query_builder = SOLRJobSearchQueryBuilder(ITEMS_PER_PAGE)
    query = query_builder.build_query(get)

    conn = Solr('http://127.0.0.1:8983/solr/')
    results = SearchResults(conn.search(**query))

    sponsored_listings = None
    if not isrobot(request):
        linkup = LinkUp()
        try:
            response = linkup.search(get_client_ip(request), get.get('q', None), get.get('loc', None), get.get('company', None))
        except:
            sponsored_listings = None
        else:
            sponsored_listings = LinkUpResults(response).sponsored_listings

    #
    # The pagination is a hack. The django paginator expects to get
    # the entire list of results and then carves out a chunk of those
    # results based on the page requested. SOLR doesn't return the 
    # entire list of results though. So we fake it to make it look
    # like it does by generating a list of size 'num_hits', filling
    # the entries for the current page with our results, and filling
    # the other entries with "don't care" values.
    #
    jobs = [ None for i in range(results.hits) ]
    page_number = int(get.get('page', '1'))

    # XXX start should be in results but pysolr doesn't included it!
    start = int(ITEMS_PER_PAGE) * (page_number - 1)
    jobs[start:start+ITEMS_PER_PAGE] = results.docs

    active_filters_vars = active_filters_context(get)
    page_vars = paginate(jobs, get, 'jobs')
    latlng_vars = latlng_context(results)

    vars = RequestContext(request, { 'facet_counts': results.facets['facet_fields'] })
    vars.update(page_vars)
    vars.update(active_filters_vars)
    vars.update(latlng_vars)
    vars.update({'sponsored_listings': sponsored_listings})

    return render_to_response('jobs/jobs.html', vars)

def jobs(request):
    """
    flat jobs list. filter job set against query parameters
    
    1. Build SOLR query
    2. Execute SOLR query
    3. Encode results in a format accessable to templates
    4. Paginate results
    5. Render template
    """
    query_builder = SOLRJobSearchQueryBuilder(ITEMS_PER_PAGE)
    query = query_builder.build_query(request.GET)

    conn = Solr('http://127.0.0.1:8983/solr/')
    results = SearchResults(conn.search(**query))

    sponsored_listings = None
    if not isrobot(request):
        linkup = LinkUp()

        q = request.GET.get('q', None) or request.GET.get('title', None)
        l = request.GET.get('loc', None)

        if l is None:
            if request.GET.get('state', None):
                if not request.GET.get('city', None):
                    l = state_abbrev_to_name(request.GET.get('state'))
                else:
                    l = request.GET.get('city').title() + ', ' + request.GET.get('state').upper()
            elif request.GET.get('country', None):
                if not request.GET.get('city', None):
                    l = country_abbrev_to_name(request.GET.get('country')).title()
                else:
                    l = request.GET.get('city').title() + ', ' + country_abbrev_to_name(request.GET.get('country')).title()
            
        c = request.GET.get('company', None)

        try:
            response = linkup.search(get_client_ip(request), q, l, c)
        except:
            sponsored_listings = None
        else:
            sponsored_listings = LinkUpResults(response).sponsored_listings

    #
    # The pagination is a hack. The django paginator expects to get
    # the entire list of results and then carves out a chunk of those
    # results based on the page requested. SOLR doesn't return the 
    # entire list of results though. So we fake it to make it look
    # like it does by generating a list of size 'num_hits', filling
    # the entries for the current page with our results, and filling
    # the other entries with "don't care" values.
    #
    jobs = [ None for i in range(results.hits) ]
    page_number = int(request.GET.get('page', '1'))

    # XXX start should be in results but pysolr doesn't included it!
    start = int(ITEMS_PER_PAGE) * (page_number - 1)
    jobs[start:start+ITEMS_PER_PAGE] = results.docs

    active_filters_vars = active_filters_context(request.GET)
    page_vars = paginate(jobs, request.GET, 'jobs')
    latlng_vars = latlng_context(results)

    vars = RequestContext(request, { 'facet_counts': results.facets['facet_fields'] })
    vars.update(page_vars)
    vars.update(active_filters_vars)
    vars.update(latlng_vars)
    vars.update({'sponsored_listings': sponsored_listings})

    return render_to_response('jobs/jobs.html', vars)

def refine_by_company(request):
    """
    Jobs grouped by company
    """
    query_builder = SOLRCompanyFacetQueryBuilder()
    query = query_builder.build_query(request.GET)

    conn = Solr('http://127.0.0.1:8983/solr/')
    results = SearchResults(conn.search(**query))

    vars = RequestContext(request, { 'facet_counts': results.facets['facet_fields'] })

    page_vars = paginate(results.facets['facet_fields']['company_id'], request.GET, 'companies')
    vars.update(page_vars)

    # replace the company names with Company objects
    companies = [ (Company.objects.get(pk=id), cnt) for id,cnt in page_vars['companies'] ]
    vars.update({ 'companies': companies })

    active_filters_vars = active_filters_context(request.GET)
    vars.update(active_filters_vars)

    latlng_vars = latlng_context(results)
    vars.update(latlng_vars)

    return render_to_response('jobs/refine_by_company.html', vars)

def refine_by_location(request):
    """
    Jobs grouped by location
    """
    query_builder = SOLRLocationFacetQueryBuilder()
    query = query_builder.build_query(request.GET)

    conn = Solr('http://127.0.0.1:8983/solr/')
    results = SearchResults(conn.search(**query))

    vars = RequestContext(request, { 'facet_counts': results.facets['facet_fields'] })

    if len(results.facets['facet_fields']['country']) > 1:
        page_vars = paginate(results.facets['facet_fields']['country'], request.GET, 'locations')
        page_vars.update({'location_field': 'country'})
    elif len(results.facets['facet_fields']['state']) > 1:
        page_vars = paginate(results.facets['facet_fields']['state'], request.GET, 'locations')
        page_vars.update({'location_field': 'state'})
    else:
        page_vars = paginate(results.facets['facet_fields']['city'], request.GET, 'locations')
        page_vars.update({'location_field': 'city'})

    vars.update(page_vars)

    active_filters_vars = active_filters_context(request.GET)
    vars.update(active_filters_vars)

    latlng_vars = latlng_context(results)
    vars.update(latlng_vars)

    return render_to_response('jobs/refine_by_location.html', vars)

ITEMS_PER_PAGE = 15

def paginate(query_set, get, object_name):
    """ 
    Paginate the results in a query set of jobs and return the 
    context variables necessary to view the paged results. 

    object_name is a string such as 'jobs', 'companies', etc. 
    that identifies the objects that are being paginated.
    """
    paginator = Paginator(query_set, ITEMS_PER_PAGE)

    #
    # Make a copy of the GET request that has 'page' 
    # removed so that 'page' and filter parameters 
    # can easily be combined in the templates
    #
    q = get.copy()
    if q.has_key('page'):
        del q['page']

    try:
        page_number = int(get['page'])
    except (KeyError, ValueError):
        page_number = 1
        
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404

    # Range of pages between first and last page to display 
    # in paginator boxes
    pages = range(max(2, page_number - 2 ), 
                  min(page_number + 2, paginator.num_pages - 1) + 1)

    return { object_name: page.object_list,
             'page': page,
             'query': q,
             'query_string': q.urlencode(),
             'pages': pages } 

def query_all():
    url = '%s/%s' % (URL, 'select/?q=*:*&wt=json')
    o = urllib.urlopen(url)
    response = json.loads(o.read())
    return response

URL = 'http://localhost:8983/solr'

def query(str):
    url = '%s/%s' % (URL, 'select/?q=' + str + '&wt=json')
    o = urllib.urlopen(url)
    response = json.loads(o.read())
    return response
    
def delete_docs(q=None):
    """
    q = query to use. If q is None then all documents are deleted
    """
    data = '{ "delete": { "query": "%s" }, "commit": {} }' % (q is not None and q or '*:*')
    hdrs = {'Content-Type': 'application/json'}

    url = '%s/update/json' % (URL,)
    req = urllib2.Request(url, data, hdrs)

    o = urllib2.urlopen(req)

def add_doc(doc):
    data = doc
    hdrs = {'Content-Type': 'application/json'}

    url = '%s/update/json' % (URL,)
    req = urllib2.Request(url, data, hdrs)

    try:
        o = urllib2.urlopen(req)
    except urllib2.HTTPError,e:
        sys.stderr.write('%s\n' % e)

def commit():
    url = '%s/update/json?commit=true' % (URL,)
    req = urllib2.Request(url)

    o = urllib2.urlopen(req)

def load_jobs(request):
    """
    View responsible for handling jobs uploaded through form
    """
    if request.method == 'POST':
        form = UploadJobsForm(request.POST, request.FILES)
        load_jobs_file(request.FILES['file'])
        if form.is_valid():
            return HttpResponse('<pre>Uploaded jobs</pre>')            
    else:
        form = UploadJobsForm()

    vars = RequestContext(request, {'form': form})
    return render_to_response('jobs/upload_jobs.html', vars)

def load_jobs_file_old(uploaded_file):
    """
    Load JSON encoded jobs file. The param uploaded_file is an 
    instance of UploadedFile.
    """
#    Company.objects.all().delete()
#    Job.objects.all().delete()
#    delete_docs()

    #
    # Get existing company object or create a new one based
    # off of contents of file. Then delete existing jobs for
    # this company from dbase to make way for new jobs.
    #
    c = json.loads(uploaded_file.read())
    company = deserialize_company_dict(c)

    if len(c['jobs']) == 0:
        return

    company.job_set.all().delete()
    delete_docs(q='company_id:%d' % company.id)

    jobs_added_successfully = []

    for j in c['jobs']:
        job = deserialize_job_dict(company, j)
        if job is not None:
            try:
                job.save()
            except _mysql_exceptions.Warning, e:
                print "job.save() generated an exception: %s" % e
            else:
                jobs_added_successfully.append(job.id)

    # XXX 
    # 
    # If the job.save() call above fails, we end up in a weird state
    # where job.id is not set. Because it's not set, we can't call
    # job.delete() to remove the job. But we can see the job if we in
    # company.job_set.all() with its id set there. We want to remove
    # the offending job and the only way seems to be to track which
    # jobs were added succesfully and remove any jobs whose id
    # doesn't show up in this list
    #
    for job in company.job_set.all():
        if job.id not in jobs_added_successfully:
            job.delete()

    index_jobs_for_company(company)

def load_jobs_file(uploaded_file):
    """
    Load JSON encoded jobs file. The param uploaded_file is an 
    instance of UploadedFile.
    """

    #
    # Get existing company object or create a new one based
    # off of contents of file. Then delete existing jobs for
    # this company from dbase to make way for new jobs.
    #
    c = json.loads(uploaded_file.read())
    company = deserialize_company_dict(c)

#    if len(c['jobs']) == 0:
#        return

    #
    # Remove all jobs for this company from SOLR. All the jobs for this company
    # will get reindexed into SOLR so we can capture any changes to the company
    # profile (since the last indexing) into the SOLR job document.
    #
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

    index_jobs_for_company(company)

def reindex_all_jobs(request):
    for company in Company.objects.all():
        delete_docs(q='company_id:%d' % company.id)
        index_jobs_for_company(company)

    return HttpResponse('<pre>Reindexed jobs</pre>')            

def reindex_jobs_for_company(request, cid):    
    """
    Reindex jobs that are already in the database back into SOLR.
    """
    company = get_object_or_404(Company, pk=cid)    
    delete_docs(q='company_id:%d' % company.id)
    index_jobs_for_company(company)
    return HttpResponse('<pre>Reindexed jobs</pre>')            

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
