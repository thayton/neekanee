#!/usr/bin/env python

import httplib

conn = httplib.HTTPSConnection("jobs.princeton.edu")
conn.request("HEAD", "/applicants/Central?delegateParameter=applicantPostingSearchDelegate&actionParameter=getJobDetail&rowId=185470&c=Sp4iSxawo6uUFrgbSFTYNA%3D%3D&pageLoadIdRequestKey=1324885025397&functionalityTableName=8192&windowTimestamp=PA_1324885023147")
res = conn.getresponse()
print res.status, res.reason
print res.getheaders()

conn = httplib.HTTPSConnection("jobs.princeton.edu")
conn.request("HEAD", "/applicants/Central?delegateParameter=applicantPostingSearchDelegate&actionParameter=getJobDetail&rowId=184632&c=cN5f1mjinXZ8ROAP6ZSy4Q%3D%3D&pageLoadIdRequestKey=1324885036772&functionalityTableName=8192&windowTimestamp=PA_1324885023147")
res = conn.getresponse()
print res.status, res.reason
print res.getheaders()

