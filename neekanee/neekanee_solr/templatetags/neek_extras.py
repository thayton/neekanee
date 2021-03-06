import re
import urllib

from isocodes import country_code_to_name
from neekanee_solr.models import CompanySize, Award
from urlparse import urlparse, urlunparse, parse_qs
from django import template
from django.http import QueryDict
from django.template.defaultfilters import stringfilter
from django.core.exceptions import ObjectDoesNotExist

numeric_test = re.compile("^\d+$")
register = template.Library()

def _qdict_del_keys(qdict, del_qstring):
    for key in del_qstring.split('&'):
        try:
            del qdict[key]
        except KeyError:
            pass
    return qdict

def _qdict_set_keys(qdict, set_qstring):
    set_qdict = QueryDict(set_qstring)
    for key, values in set_qdict.items():
        qdict[key] = set_qdict[key]
    return qdict

def qstring_del(qstring, del_qstring):
    """
    Returns a query string w/o some keys, every value for each key gets deleted.

    More than one key can be specified using an & as separator:

    {{ qstring|qstring_del:"key1&key2" }}

    Remove the tags key from the current query string:

    {{ query.urlencode|qstring_del:"tags" }}
    """
    qdict = QueryDict(qstring, mutable=True)
    return _qdict_del_keys(qdict, del_qstring).urlencode()


def qstring_set(new_qstring, old_qstring):
    """
    Updates a query string, old values get deleted.

    {{ new_qstring|qstring_set:old_qstring }}

    {{ "key1=1&key1=2&key2=3"|qstring_set:query.urlencode }}
    """
    old_qdict = QueryDict(old_qstring, mutable=True)
    return _qdict_set_keys(old_qdict, new_qstring).urlencode()

def getattribute(value, arg):
    """ 
    Gets an attribute of an object dynamically from a string name 
    Reference: http://stackoverflow.com/questions/844746/performing-a-getattr-style-lookup-in-a-django-template
    """
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)

def award_string(value):
    try:
        award = Award.objects.get(pk=value)
        return award.name
    except ObjectDoesNotExist:
        return value

def company_size_string(value):
    try:
        company_size = CompanySize.objects.get(pk=value)
        if company_size.lo == 10001:
            return '%d+' % (company_size.lo - 1)
        else:
            return '%d-%d' % (company_size.lo, company_size.hi)

    except ObjectDoesNotExist:
        return value

def append(value, arg):
    """
    Append arg to value list
    """
    value.append(arg)
    return value

@stringfilter
def encode_ampersand(str):
    return str.replace('&', '%26')

@stringfilter
def truncatestr(str, cnt):
    try:
        if len(str) > cnt + len('...'):
            return str[:int(cnt)] + '...'
        else:
            return str
    except:
        return value
    
@stringfilter
def remove_scheme(url):
    u = urlparse(url)
    l = len(u.scheme + '://')
    return url[l:]
    
@stringfilter
def prepend(value, arg):
    """
    Usage: "Doe"|prepend:"John"
    """
    return arg + value

def add_tag(query_tags, tag):
    tags = [ x.replace('&', '%26') for x in query_tags.split() ]
    tag = tag.replace('&', '%26')

    if tag not in tags:
        tags.append(tag)
    
    tags = '+'.join(tags)
    return 'tags=' + tags

# XXX Just the same as add_tag but uses 'ltag=' instead of 'tag'
# so we should refactor this
def add_location_tag(query_tags, tag):
    tags = [ x.replace('&', '%26') for x in query_tags.split() ]
    tag = tag.replace('&', '%26')

    if tag not in tags:
        tags.append(tag)
    
    tags = '+'.join(tags)
    return 'ltags=' + tags

@stringfilter
def split(value, arg=None):
    return value.split()

@stringfilter
def split_and_remove(value, arg):
    list = value.split()
    if arg in list:
        list.remove(arg)
    return list

@stringfilter
def urlquote(value):
    return urllib.quote(value, '/=')

def q_to_query_dict(value):
    return QueryDict(value)

@stringfilter
def parse_url_qs(value):
    """ 
    Extract the query string from a URL, then parse the
    query string and return the dictionary result.
    """
    return parse_qs(value, keep_blank_values=True).items()

@stringfilter
def parse_url_qs_dict(value):
    """ 
    Extract the query string from a URL, then parse the
    query string and return the dictionary result.
    """
    return parse_qs(value, keep_blank_values=True)

@stringfilter
def capwords(value):
    """
    Capitalizes the first characters of each word in value.
    """
    return value and \
        ' '.join([ x[0].upper() + x[1:] for x in value.lower().split() ])

capwords.is_safe=True

def modulus(value, arg):
    try:
        return int(value) % int(arg)
    except (ValueError, TypeError):
        return value
    
def divide(value, arg):
    """
    Divides the value by arg.

    Usage: 10|divide:"2"
    """
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError):
        return value

def subtract(value, arg):
    return int(value) - int(arg)

def empcnt_numtorange(value):
    """ 
    Convert employee count number to range 
    XXX Use a separate table for employee count
    ranges so you don't have to do this 
    """
    ranges = [ "1-10",
               "11-50",
               "51-200",
               "201-500",
               "501-1000",
               "1001-5000",
               "5001-10000",
               "10,001+" ]

    try:
        return ranges[value - 1]
    except (ValueError, TypeError):
        return value

COUNTRY_ABBREV_TO_NAME = {
    'US': 'United States',
    'FR': 'France'
}

STATE_ABBREV_TO_NAME = {
    'AL': "Alabama",
    'AK': "Alaska",
    'AZ': "Arizona",
    'AR': "Arkansas",
    'CA': "California",
    'CO': "Colorado",
    'CT': "Connecticut",
    'DE': "Delaware",
    'DC': "District of Columbia",
    'D.': "District of Columbia",
    'FL': "Florida",
    'GA': "Georgia",
    'HA': "Hawaii",
    'HI': "Hawaii",
    'ID': "Idaho",
    'IL': "Illinois",
    'IN': "Indiana",
    'IA': "Iowa",
    'KS': "Kansas",
    'KY': "Kentucky",
    'LA': "Louisiana",
    'LO': "Louisiana",
    'ME': "Maine",
    'MD': "Maryland",
    'MA': "Massachusetts",
    'MI': "Michigan",
    'MN': "Minnesota",
    'MS': "Mississippi",
    'MO': "Missouri",
    'MT': "Montana",
    'NE': "Nebraska",
    'NV': "Nevada",
    'NH': "New Hampshire",
    'NJ': "New Jersey",
    'NM': "New Mexico",
    'NY': "New York",
    'NC': "North Carolina",
    'ND': "North Dakota",
    'OH': "Ohio",
    'OK': "Oklahoma",
    'OR': "Oregon",
    'PA': "Pennsylvania",
    'RI': "Rhode Island",
    'SC': "South Carolina",
    'SD': "South Dakota",
    'TN': "Tennessee",
    'TX': "Texas",
    'UT': "Utah",
    'VT': "Vermont",
    'VA': "Virginia",
    'WA': "Washington",
    'WV': "West Virginia",
    'WI': "Wisconsin",
    'WY': "Wyoming"
}

def state_abbrev_to_name(value):
    try:
        return STATE_ABBREV_TO_NAME[value.upper()]
    except:
        return value

def country_abbrev_to_name(value):
    try:
        return country_code_to_name[value.lower()]
    except:
        return value

register.filter('truncatestr', truncatestr)
register.filter('remove_scheme', remove_scheme)    
register.filter('append', append)    
register.filter('prepend', prepend)    
register.filter('split', split)
register.filter('split_and_remove', split_and_remove)
register.filter('parse_url_qs', parse_url_qs)
register.filter('parse_url_qs_dict', parse_url_qs_dict)
register.filter('state_abbrev_to_name', state_abbrev_to_name)
register.filter('country_abbrev_to_name', country_abbrev_to_name)
register.filter('subtract', subtract)
register.filter('divide', divide)
register.filter('modulus', modulus)
register.filter('capwords', capwords)
register.filter('empcnt_numtorange', empcnt_numtorange)
register.filter('award_string', award_string)
register.filter('company_size_string', company_size_string)
register.filter('get_range', get_range)
register.filter('getattribute', getattribute)
register.filter('qstring_del', qstring_del)
register.filter('qstring_set', qstring_set)
register.filter('urlquote', urlquote)
register.filter('encode_ampersand', encode_ampersand)
register.filter('add_tag', add_tag)
register.filter('add_location_tag', add_location_tag)
register.filter('q_to_query_dict', q_to_query_dict)
