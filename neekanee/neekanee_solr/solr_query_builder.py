KM_PER_MILE = 1.61

class SOLRQueryBuilder():
    """
    Build a SOLR query given a GET QueryDict for a job search.
    """
    def __init__(self):
        self.qdict = {}

        #
        # Mapping of refine search query parameter names to SOLR doc 
        # field names. All refine search query parameters are implemented 
        # as filter queries. For each param in GET from the left column
        # below, we add a new filter query using the field name in the
        # right column and value GET[param].
        #
        self.refine_search_fq = {
        #
        #    param     SOLR field name
        #    -----     ---------------
            'tld':      'tld',
            'title':    'title',
            'company':  'company_name',
            'size':     'company_size',
            'tags':     'company_tags',
            'ltags':    'company_location_tags',
            'awards':   'company_awards',
            'vacation': 'vacation_year_1',
            'country':  'country',
            'state':    'state',
            'city':     'city',
        }

    def add_fq(self, filt, val):
        if filt != 'vacation_year_1':
            new_fq = '%s:"%s"' % (filt,val)
        else:
            new_fq = '%s:%s' % (filt,val)

        if self.qdict.has_key('fq'):
            self.qdict['fq'].append(new_fq)
        else:
            self.qdict['fq'] = [new_fq]
        
    def build_query(self, GET):
        """
        GET : QueryDict object for an HTTP GET request
        """
        self.qdict['q'] = '{!q.op=AND}' + GET.get('q', '*:*')
        self.qdict['wt'] = 'json'

        if 'lat' in GET and 'lng' and GET:
            self.qdict['fq'] = [ '{!bbox}' ]
            self.qdict['sfield'] = 'latlng'
            self.qdict['pt'] = '%.2f,%.2f' % (float(GET['lat']),float(GET['lng']))
            self.qdict['d'] = '%.2f' % (float(GET['radius']) * KM_PER_MILE)

        for parm,filt in self.refine_search_fq.items():
            val = GET.get(parm, None)
            if val is None:
                continue

            if parm == 'tags' or parm == 'ltags' or parm == 'awards': # multivalued
                for v in val.split():
                    self.add_fq(filt, v)
            elif parm == 'vacation':
                self.add_fq(filt, '[%d TO %d]' % (int(val), int(val)+4))
            else:
                self.add_fq(filt, val)

        return self.qdict

class SOLRJobSearchQueryBuilder(SOLRQueryBuilder):
    def __init__(self, items_per_page):
        SOLRQueryBuilder.__init__(self)
        self.items_per_page = items_per_page

        #
        # Pararms specific to job search query with faceting for the
        # sidebar. The state facet field is set to 51 so that all of
        # the states will show up in the map (and not just 10 of them).
        #
        params = {
            'fl': 'id,title,url,url_data,company_id,company_name,company_ats,company_jobs_page_url,city,state,country',
            'facet': 'true',
            'facet.field': ['country', 'state', 'city', 'tld', 'company_size', 'company_name', 'company_tags', 'company_location_tags', 'company_awards'], 
            'facet.mincount': '1',
            'facet.limit': '10',
            'f.company_tags.facet.limit': '32',
            'f.country.facet.limit': '200',
            'f.state.facet.limit': '51',
            'facet.range': 'vacation_year_1',
            'facet.range.start': '10',
            'facet.range.end': '50',
            'facet.range.gap': '5',
            'hl': 'true',
            'hl.fl': 'desc',
            'hl.snippets': 2,
            'hl.alternateField': 'desc',
            'hl.maxAlternateFieldLength': '210',
            'rows': '%d' % self.items_per_page
        }
        self.qdict.update(params)

    def build_query(self, GET):
        page_number = int(GET.get('page', '1'))
        self.qdict.update({'start': '%d' % (self.items_per_page * (page_number - 1))})
        return SOLRQueryBuilder.build_query(self, GET)

class SOLRCompanyFacetQueryBuilder(SOLRQueryBuilder):
    def __init__(self):
        SOLRQueryBuilder.__init__(self)

        params = {
            'fl': 'id',
            'facet': 'true',
            'facet.field': ['country', 'state', 'city', 'tld', 'company_size', 'company_tags', 'company_location_tags', 'company_awards', 'company_id'], 
            'facet.mincount': '1',
            'facet.limit': '10',
            'facet.range': 'vacation_year_1',
            'facet.range.start': '10',
            'facet.range.end': '50',
            'facet.range.gap': '5',
            'f.company_tags.facet.limit': '32',
            'f.country.facet.limit': '200',
            'f.state.facet.limit': '51',
            'f.company_id.facet.limit': '-1'
        }
        self.qdict.update(params)

    def build_query(self, GET):
        return SOLRQueryBuilder.build_query(self, GET)

class SOLRLocationFacetQueryBuilder(SOLRQueryBuilder):
    def __init__(self):
        SOLRQueryBuilder.__init__(self)

        params = {
            'fl': 'id',
            'facet': 'true',
            'facet.field': ['country', 'state', 'city', 'tld', 'company_size', 'company_name', 'company_tags', 'company_location_tags', 'company_awards'], 
            'facet.mincount': '1',
            'facet.limit': '10',
            'facet.range': 'vacation_year_1',
            'facet.range.start': '10',
            'facet.range.end': '50',
            'facet.range.gap': '5',
            'f.company_tags.facet.limit': '32',
            'f.country.facet.limit': '200',
            'f.state.facet.limit': '60',
            'f.city.facet.limit': '-1'
        }
        self.qdict.update(params)

    def build_query(self, GET):
        return SOLRQueryBuilder.build_query(self, GET)

class SOLRJobTitleFacetQueryBuilder(SOLRQueryBuilder):
    pass

