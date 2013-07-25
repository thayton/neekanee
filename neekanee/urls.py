import os
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from neekanee_solr.templatetags.isocodes import state_abbrev_to_name

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

states_regex = '(?:' + '|'.join(['%s' % s.lower() for s in state_abbrev_to_name.keys()])

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     { 'document_root': os.path.join(os.path.dirname(__file__), 'neekanee_solr/media/') }),

#    (r'^logout/$',         'django.contrib.auth.views.logout', {'next_page': '/'}),
#    (r'',                  include('django.contrib.auth.urls')),
    (r'^admin/',           include(admin.site.urls)),
)

urlpatterns += patterns('neekanee.neekanee_solr.views',
    # Example:
    # (r'^jobsearch/', include('jobsearch.foo.urls')),

    (r'^$',        direct_to_template, { 'template': 'index.html'   }),
    (r'^about$',   direct_to_template, { 'template': 'about.html'   }),
    (r'^contact$', direct_to_template, { 'template': 'contact.html' }),
    (r'^help$',    direct_to_template, { 'template': 'help.html'    }),

    (r'^search/',           'search'),
    (r'^jobs/$',            'jobs'),
    (r'^jobs/(?P<jobid>[0-9]+)$', 'job'),
    (r'^job_alerts/',       'job_alerts'),
    (r'^jobs_by_company/',  'refine_by_company'),
    (r'^jobs_by_location/', 'refine_by_location'),

    (r'^browse_jobs/$',                                 'browse_jobs'),
    (r'^browse_jobs/by_category/(?P<category>[^/]+)/$', 'browse_jobs_by_category'),                        
    (r'^browse_jobs/by_company/(?P<name>\w)/$',         'browse_jobs_by_company'),
    (r'^browse_jobs/by_job_title/(?P<title>\w)/',       'browse_jobs_by_job_title'),

    (r'^companies/$',                       'companies'),
    (r'^companies/(?P<cid>\d+)/$',          'company'),
    (r'^companies/(?P<cslug>[a-z0-9-]+)/$', 'company'),

    # Upload jobs via POST
    (r'^load_jobs/', 'load_jobs'),
    (r'^reindex_jobs_for_company/(?P<cid>\d+)/$', 'reindex_jobs_for_company'),
    (r'^reindex_all_jobs/$',                      'reindex_all_jobs'),

    # User management
    (r'^account/',                                         include('allauth.urls')),
    (r'^account/profile/$',                                'user_profile'),

    (r'^account/job_alerts/$',                             'user_job_alerts'),
    (r'^account/job_alerts/create/(?P<query>[^/]+)/$',     'create_job_alert'),
    (r'^account/job_alerts/(?P<alert_id>\d+)/delete/$',    'delete_job_alert'),
    (r'^account/job_alerts/(?P<alert_id>\d+)/edit/$',      'edit_job_alert'),
    (r'^delete_job_alert/(?P<alert_key>\w+)$',             'delete_job_alert_from_email'),

    (r'^account/job_basket/$',                             'user_job_basket'),
    (r'^account/job_basket/add/(?P<job_id>\d+)/$',         'add_job_to_basket'),
    (r'^account/job_basket/(?P<bookmark_id>\d+)/delete/$', 'delete_job_from_basket'),

    # SEO-friendly URL scheme
    #-----------------------------------------------------------------
    # Fix for broken BBT links
    (r'jobs-at-bb$',       'broken_bbt_links'),
    (r'jobs-at-bb-in-',    'broken_bbt_links'),
    (r'jobs-at-bb26t$',    'broken_bbt_links'),
    (r'jobs-at-bb26t-in-', 'broken_bbt_links'),

    # Fix for broken University of Miami links
    (r'jobs-at-universiy-of-miami', 'broken_miami_edu_links'),

    (r'^jobs-in-(?P<city>[a-z0-9-+]+)-(?P<state>[a-z]{2})-(?P<country>us)$', 'seosearch'),
    (r'^jobs-in-(?P<state>[a-z]+)-(?P<country>us)$',                         'seosearch'),
    (r'^jobs-in-(?P<city>[a-z0-9-]+)-(?P<country>[a-z]{2})$',                'seosearch'),
    (r'^jobs-in-(?P<country>[a-z]{2})$',                                     'seosearch'),

    (r'^jobs-at-(?P<cslug>[a-z0-9-]+)-in-(?P<city>[a-z0-9-]+)-(?P<state>[a-z]{2})-(?P<country>us)$', 'seosearch'),
    (r'^jobs-at-(?P<cslug>[a-z0-9-]+)-in-(?P<state>[a-z]{2})-(?P<country>us)$',                      'seosearch'),
    (r'^jobs-at-(?P<cslug>[a-z0-9-]+)-in-(?P<city>[a-z0-9-]+)-(?P<country>[a-z]{2})$',               'seosearch'),
    (r'^jobs-at-(?P<cslug>[a-z0-9-]+)-in-(?P<country>[a-z]{2})$',                                    'seosearch'),
    (r'^jobs-at-(?P<cslug>[a-z0-9-]+[a-z0-9])$',                                                     'seosearch'),

    (r'(?P<q>[^/]+)-jobs-in-(?P<city>[a-z0-9-]+)-(?P<state>[a-z]{2})-(?P<country>us)$', 'seosearch'),
    (r'(?P<q>[^/]+)-jobs-in-(?P<state>[a-z]{2})-(?P<country>us)$',                      'seosearch'),
    (r'(?P<q>[^/]+)-jobs-in-(?P<city>[a-z0-9-]+)-(?P<country>[a-z]{2})$',               'seosearch'),
    (r'(?P<q>[^/]+)-jobs-in-(?P<country>[a-z]{2})$',                                    'seosearch'),

    (r'(?P<q>[^/]+)-jobs$',                                                                                      'seosearch'),
    (r'(?P<q>[^/]+)-jobs-at-(?P<cslug>[a-z0-9-]+)-in-(?P<city>[a-z0-9-]+)-(?P<state>[a-z]{2})-(?P<country>us)$', 'seosearch'),
    (r'(?P<q>[^/]+)-jobs-at-(?P<cslug>[a-z0-9-]+)-in-(?P<state>[a-z]{2})-(?P<country>us)$',                      'seosearch'),
    (r'(?P<q>[^/]+)-jobs-at-(?P<cslug>[a-z0-9-]+)-in-(?P<city>[a-z0-9-]+)-(?P<country>[a-z]{2})$',               'seosearch'),
    (r'(?P<q>[^/]+)-jobs-at-(?P<cslug>[a-z0-9-]+)-in-(?P<country>[a-z]{2})$',                                    'seosearch'),    
    (r'(?P<q>[^/]+)-jobs-at-(?P<cslug>[a-z0-9-]+[a-z0-9])$',                                                     'seosearch'),

    # Fix for all of the broken links in GWT that end in <state>-                        
    (r'^jobs-in\S*-' + states_regex + ')-$',                    'broken_states_links'),                        
    (r'^jobs-at-[a-z0-9-]+-in\S*-' + states_regex + ')-$',      'broken_states_links'),
    (r'[^/]+-jobs-in\S*-' + states_regex + ')-$',               'broken_states_links'),
    (r'[^/]+-jobs-at-[a-z0-9-]+-in\S*-' + states_regex + ')-$', 'broken_states_links'),
    (r'-in-\S+-$', 'broken_city_links')
    #-----------------------------------------------------------------

#    (r'^register/$',                                        'register_page'),
#    (r'^register/success/$', direct_to_template, { 'template': 'registration/register_success.html' }),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    (r'^admin/', include(admin.site.urls)),
)
