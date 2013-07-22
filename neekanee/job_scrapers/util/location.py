import string
import re

######################################################################
# Location strings come in many different formats:
#
# Mountain View or Chatsworth, CA, USA
# Washington, DC
# MD-Ft. Detrick
# VA-Falls Church
# HI-Honolulu
# MD-Ft. Detrick
# Rockville, MD
# Bethesda, Maryland
# Buffalo, NY (Corporate Headquarters)
######################################################################
STATES = (
    ('ALABAMA'              , 'AL'),
    ('ALASKA'               , 'AK'),
    ('ARIZONA'              , 'AZ'),
    ('ARKANSAS'             , 'AR'),
    ('CALIFORNIA'           , 'CA'),
    ('COLORADO'             , 'CO'),
    ('CONNECTICUT'          , 'CT'),
    ('DELAWARE'             , 'DE'),
    ('DISTRICT OF COLUMBIA' , 'DC'),
    ('DISTRICT OF COLUMBIA' , 'D\.C\.'),
    ('FLORIDA'              , 'FL'),
    ('GEORGIA'              , 'GA'),
    ('HAWAII'               , 'HI'),
    ('IDAHO'                , 'ID'),
    ('ILLINOIS'             , 'IL'),
    ('INDIANA'              , 'IN'),
    ('IOWA'                 , 'IA'),
    ('KANSAS'               , 'KS'),
    ('KENTUCKY'             , 'KY'),
    ('LOUISIANA'            , 'LA'),
    ('MAINE'                , 'ME'),
    ('MARYLAND'             , 'MD'),
    ('MASSACHUSETTS'        , 'MA'),
    ('MICHIGAN'             , 'MI'),
    ('MINNESOTA'            , 'MN'),
    ('MISSISSIPPI'          , 'MS'),
    ('MISSOURI'             , 'MO'),
    ('MONTANA'              , 'MT'),
    ('NEBRASKA'             , 'NE'),
    ('NEVADA'               , 'NV'),
    ('NEW HAMPSHIRE'        , 'NH'),
    ('NEW JERSEY'           , 'NJ'),
    ('NEW MEXICO'           , 'NM'),
    ('NEW YORK'             , 'NY'),
    ('NORTH CAROLINA'       , 'NC'),
    ('NORTH DAKOTA'         , 'ND'),
    ('OHIO'                 , 'OH'),
    ('OKLAHOMA'             , 'OK'),
    ('OREGON'               , 'OR'),
    ('PENNSYLVANIA'         , 'PA'),
    ('RHODE ISLAND'         , 'RI'),
    ('SOUTH CAROLINA'       , 'SC'),
    ('SOUTH DAKOTA'         , 'SD'),
    ('TENNESSEE'            , 'TN'),
    ('TEXAS'                , 'TX'),
    ('UTAH'                 , 'UT'),
    ('VERMONT'              , 'VT'),
    ('VIRGINIA'             , 'VA'),
    ('WASHINGTON'           , 'WA'),
    ('WEST VIRGINIA'        , 'WV'),
    ('WISCONSIN'            , 'WI'),
    ('WYOMING'              , 'WY'))

CITY_RE = r'(\w+\.?( \w+\.?){0,3})'
STABBR_RE = '(' + r'|'.join([ r'\b%s\.?\b' % (a) for n,a in STATES ]) + ')'
STNAME_RE = '(' + r'|'.join([ r'%s'        % (n) for n,a in STATES ]) + ')'

def strip_nonascii(s):
    return filter(lambda x: x in string.printable, s)

def state_name_to_abbrev(name):
    for stname, stabbr in STATES:
        if name == stname:
            return stabbr

#
# Regular expression search for location l. If found returns
# match group m. Select groups from m which correspond to city, state
#
CITY_STATE_RE = (
    #
    # Rockville, MD
    # Rockville , MD
    #
    (
        lambda l: re.search(CITY_RE + r'\W?,\W?' + STABBR_RE + r'$', l),
        lambda m: m.group(1),
        lambda m: m.group(3)
    ),
    #
    # Rockville, Maryland
    #
    (
        lambda l: re.search(CITY_RE + r'\W?,\W?' + STNAME_RE + r'$', l),
        lambda m: m.group(1),
        lambda m: state_name_to_abbrev(m.group(3))
    ),
    #
    # Rockville-Maryland
    #
    (
        lambda l: re.search(CITY_RE + r'-\W?' + STNAME_RE + r'$', l),
        lambda m: m.group(1),
        lambda m: state_name_to_abbrev(m.group(3))
    ),
    #
    # Rockville-MD
    #
    (
        lambda l: re.search(CITY_RE + r'-\W?' + STABBR_RE + r'$', l),
        lambda m: m.group(1),
        lambda m: m.group(3)
    ),
    #
    # Rockville MD
    # 
    (
        lambda l: re.search(CITY_RE + r'\W+' + STABBR_RE + r'$', l),
        lambda m: m.group(1),
        lambda m: m.group(3)
    ),

    #
    # Rockville Maryland
    # 
    (
        lambda l: re.search(CITY_RE + r'\W+' + STNAME_RE + r'$', l),
        lambda m: m.group(1),
        lambda m: state_name_to_abbrev(m.group(3))
    ),

    #
    # Maryland, Rockville
    # Maryland , Rockville
    #
    (
        lambda l: re.search(STNAME_RE + r'\W?,\W?' + CITY_RE + r'$', l),
        lambda m: m.group(2),
        lambda m: state_name_to_abbrev(m.group(1))
    ),

    #
    # MD-Rockville
    # MD - Rockville
    #
    (
        lambda l: re.search(STABBR_RE + r'\W?-\W?' + CITY_RE + r'$', l),
        lambda m: m.group(2),
        lambda m: m.group(1)
    ),

    #
    # MD:Rockville
    # MD: Rockville
    #
    (
        lambda l: re.search(STABBR_RE + r'\W?:\W?' + CITY_RE + r'$', l),
        lambda m: m.group(2),
        lambda m: m.group(1)
    ),

    #
    # FL, Jacksonville
    # FL,Jacksonville
    #
    (
        lambda l: re.search(STABBR_RE + r'\W?,\W?' + CITY_RE + r'$', l),
        lambda m: m.group(2),
        lambda m: m.group(1)
    ),

    # Maryland-Rockville
    # Maryland - Rockville
    #
    (
        lambda l: re.search(STNAME_RE + r'\W?-\W?' + CITY_RE + r'$', l),
        lambda m: m.group(2),
        lambda m: state_name_to_abbrev(m.group(1))
    ),

    #
    # New Jersey
    # New York
    #
    (
        lambda l: re.search(STNAME_RE + r'$', l),
        lambda m: None,
        lambda m: state_name_to_abbrev(m.group(1))
    )
)

def parse_location(location):
    import neekgeocoder
    return neekgeocoder.geocode(location)

def parse_location_old(location):
    location = location.strip().upper()
    location = location.replace('&NBSP;', '')
    location = strip_nonascii(location)

    for lsearch, getcity, getstate in CITY_STATE_RE:
        m = lsearch(location)
        if m and m.lastindex > 1:
            city, state = getcity(m), getstate(m)

            if city and state:
                l =  {'city': city.lower(), 
                      'state': state.lower(),
                      'country': 'us'}

                print "--> Location: %s => %s" % (location, l)
                return l

            #
            # XXX TODO
            # Handle state only (eg. New Jersey)
            # Handle city only (eg. Chicago)
            # Handle regions (eg. Southern California)
            #

if __name__ == '__main__':
    l = parse_location('Rockville, MD')
    print l

    l = parse_location('Rockville , MD')
    print l

    l = parse_location('Rockville, Maryland')
    print l

    l = parse_location('Rockville , Maryland')
    print l

    l = parse_location('Rockville MD')
    print l

    l = parse_location('Rockville Maryland')
    print l

    l = parse_location('Rockville-MD')
    print l

    l = parse_location('MD-Rockville')
    print l

    l = parse_location('MD-Havre De Grace')
    print l

    l = parse_location('California, Campbell')
    print l

    l = parse_location('New Jersey')
    print l

    l = parse_location('New York, New York')
    print l

    l = parse_location('New York')
    print l

    l = parse_location('Frederick, Maryland ')
    print l

