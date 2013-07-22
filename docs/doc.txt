Loading Backup Data
===================
To load backup data generated using django's dumpdata command first
set the pk field to NULL in the files to be loaded. In VI, this can
be done with the following command::

  s/"pk": [0-9]\+/"pk": null/g

Then use python manage.py loaddata <file> to import the data.

Scraping Jobs
=============
links = scrape job links

# remove dead job links
for each job currently in database:
  if job not in links:
    delete job

# only retrieve descriptions for jobs not already in database
for each link in links:
  if link not in job database:
    retrieve job description
    save job

export / serialize list of company jobs for uploading to webhost

Note that for sites that only use fragment IDs or no links at all
for job postings, then all existing jobs should be deleted before
scraping new jobs::

  self.company.job_set.all().delete()

Check that plugins that don't call self.prune_unlisted_jobs() that 
a call is made to self.company.job_set.all().delete() instead.
  
Importing / Deserializing Jobs
==============================
import new list of all jobs for company

# remove dead job links
for each job currently in database:
  if job not in new list:
    delete job

# only import descriptions for jobs not already in database
for each job in job list:
  if job not already in database

Requirements
============
1. MySQLdb
   http://sourceforge.net/projects/mysql-python/

   Required by load_xml_results.py in order to upload
   jobs into the database.

2. BeautifulSoup
   http://www.crummy.com/software/BeautifulSoup/

3. Mechanize
   http://wwwsearch.sourceforge.net/mechanize/

4. pdftohtml
   http://pdftohtml.sourceforge.net/

5. Javascript
   Need to use SpiderMonkey or some kind of
   JavaScript library in order to handle pages
   like http://www.poweredbytippr.com/about-the-company/careers/
   that generate the job listings using JavaScript.
   Right now we can't parse these pages.

6. Some additional tools for scraping sites are here::
   http://www.zejack.com/article/linux/slackware/htdig-3.1.6.html
   swf2html tool (Linux/Unix variant?)

7. geopy
   Needed for geocoding locations and calculating distances 
   between locations:
   Available at http://code.google.com/p/geopy/

8. pdftotext
   http://foolabs.com/xpdf/download.html
   An alternative to pdftohtml. Part of the Xpdf suite.

9. SOLR
   Used to do the actual searching

   For security configure jetty.xml to only listen on 127.0.0.1
   by setting::

     <Set name="host"><SystemProperty name="jetty.host" default="127.0.0.1" /></Set>

   Follow this guide in order to daemonize SOLR::

     http://stackoverflow.com/questions/2150767/how-to-start-solr-automatically

10. OAuth / LinkedIn

    API Key: 3hrs63w15aim       
    Secret Key: KbsiF1QOM78UaL9U

Plugins
=======

Supported Formats
-----------------
1. HTML

2. PDF

The crawler uses the utility pdftohtml in order to convert job descriptions
in PDF to HTML. The utility must be installed on the system running the crawler.

3. MS Word

AbiWord (http://www.abisource.com/) has a command line utility abiword that
can be used to convert word documents into HTML but this feature doesn't 
seem to be available for Macs.

Once MS Word support is added the site http://www.some.org/about_jobs.html
has jobs in Word format for testing.

The following site details one method for converting a Word document into
HTML using Abi Word:

http://bitkickers.blogspot.com/2010/12/python-convert-wordpdf-document-to-html.html

4. Flash

Need to see what options are available for parsing Flash sites. Once found check
out Novartis's job page as it uses flash:

http://www.novartis.com/careers/job-search/index.shtml

Different Types of Plugins
--------------------------

1. Plugins that follow a link to get to the job description

2. Plugins that follow a fragment identifier to get to the job description

3. Plugins that scrape a single page for both job title and job description

4. Plugins that interact with an Applicant Tracking System

Tips
----
Things to remove from URLs when scraping plugins:

1. Timestamps (eg. peopleadmin)
2. Session IDs (Kenexa)
3. Page numbers (Apple)
4. Params (eg. Taleo)

In general try to figure out the minimal amount of query parameters required
for the URL to still work. When testing the URL in a browser, clear all 
cookies/state to verify there are no cookie dependencies for the URL to work.

Applicant Tracking Systems
==========================

1. Taleo

2. Brassring / Kenexa

The sites that use Kenexa require you to already have a cookie from the 
job site in order to view a job description. If you follow a link from 
Neekanee to the job ad, and your browser doesn't have a cookie for the 
site using Kenexa to advertise the job, then the site will return an 
error. The error will show up in the title bar as 'Cookies Disabled'.
The URL will also be redirected (302 Object Moved) from the URL of the 
job description to one that reports that error::

  https://sjobs.brassring.com/1033/ASP/TG/cim_NoBrandError.asp?ErrMsg=NoCookieGetSessionIdForXML

In reality the page at this new URL shows up blank but if we look at
the source for the page it's clear that the site thinks we have 
cookies disabled::

  <html>
    <head>
      <title>Cookies disabled</title>
    </head>
    <body>
      <p>
        <table width="90%" align=center cellPadding=0 cellSpacing=0>
          <tbody>
            <tr>
              <td vAlign=center><br><br>
                <p align=left><font size="2"></font></p>
              <td></td>
            </tr>
          </tbody>
        </table>
      </p>
    </body>
  </html>

If a user were browsing the job site directly, this wouldn't be an 
issue, since in the course of browsing the cookie would be downloaded. 
For Neekanee to provide links to job descriptions though, it means we 
must either serve a third-party cookie for Kenexa sites, or somehow 
serve up a cookie for the Kenexa site being linked to. 

The current (partial) solution is to load a portion of the site being
linked to in a hidden iframe. The site being linked to then delivers
the cookie via the iframe. Then when the user clicks on the job link,
the cookie is already in place and the link works::

  <iframe src="http://www.viasat.com/careers/openings" width="1" height="1"></iframe>

The above iframe would cause the src page to be loaded. When loaded, the 
src page serves a cookie which is then saved on the browser. When the
user clicks on one of the ViaSat job links, that cookie will be sent to
the server and the user will be able to view the job ad. Without the cookie,
the user would instead see an error page indicating that 'Cookies aren't 
enabled.'

This breaks on some browsers like Safari though, where the setting
'Only from sites I visit' may be enabled. In this case, Safari won't
accept the cookies delivered from the page loaded in the iframe.

Alternate solution may be to create a form whose target is the iframe, and
then use JavaScript to submit the form using POST as the method. The HTML
below shows how to do this with a manually submitted form::

  <form action="https://careers.netapp.com/1033/ASP/TG/cim_home.asp?partnerid=25093&siteid=5100" method="POST" target="my_iframe">
    <input type="submit" value="Submit" />
  </form>
  <iframe name="my_iframe" src="https://careers.netapp.com/1033/ASP/TG/cim_home.asp?partnerid=25093&siteid=5100" width="1" height="1"></iframe>

  <a href="https://careers.netapp.com/1033/ASP/TG/cim_jobdetail.asp?SID=%5EDIwxWycGP0DWYjzK23407mS1yk/yZT7y23FFRWHQnNSW3souYhwPFY/ZT5XkI9kJ&jobId=214018&type=search&JobReqLang=1&recordstart=451&JobSiteId=5100&JobSiteInfo=214018_5100&GQId=0">Sales Representative</a>

Before the Submit button is pressed, the link the Sales Rep job won't work and the
user will get a 'Cookies Disabled' error. Once the Submit button is pressed though
the cookies from netapp.com will get stored onto the browser and then the link
will work correctly.

The JavaScript code to automatically submit a form, without a user having to press 
the Submit button is shown below::

  <script type="text/javascript">
    function myfunc() {
      var frm = document.getElementById("my_form");
      frm.submit();
    }
    window.onload = myfunc;
  </script>

All of the required HTML then becomes::

  <html>
    <form id="my_form" action="https://careers.netapp.com/1033/ASP/TG/cim_home.asp?partnerid=25093&siteid=5100" method="POST" target="my_iframe">
    </form>

    <iframe name="my_iframe" src="https://careers.netapp.com/1033/ASP/TG/cim_home.asp?partnerid=25093&siteid=5100" width="1" height="1"></iframe>

    <script type="text/javascript">
      function myfunc() {
        var frm = document.getElementById("my_form");
        frm.submit();
      }
      window.onload = myfunc;
    </script>

    <a href="https://careers.netapp.com/1033/ASP/TG/cim_jobdetail.asp?SID=%5EDIwxWycGP0DWYjzK23407mS1yk/yZT7y23FFRWHQnNSW3souYhwPFY/ZT5XkI9kJ&jobId=214018&type=search&JobReqLang=1&recordstart=451&JobSiteId=5100&JobSiteInfo=214018_5100&GQId=0">Sales Representative</a>
  </html>

This can be shortened to::

  <html>
    <body onload="document.forms['my_form'].submit();">
      <form id="my_form" action="https://careers.netapp.com/1033/ASP/TG/cim_home.asp?partnerid=25093&siteid=5100" method="POST" target="my_iframe">
      </form>

      <iframe name="my_iframe" src="https://careers.netapp.com/1033/ASP/TG/cim_home.asp?partnerid=25093&siteid=5100" style="visibility:hidden" width="1" height="1"></iframe>

      <a href="https://careers.netapp.com/1033/ASP/TG/cim_jobdetail.asp?SID=%5EDIwxWycGP0DWYjzK23407mS1yk/yZT7y23FFRWHQnNSW3souYhwPFY/ZT5XkI9kJ&jobId=214018&type=search&JobReqLang=1&recordstart=451&JobSiteId=5100&JobSiteInfo=214018_5100&GQId=0">Sales Representative</a>
    </body>
  </html>

Use style="visibility:hidden" to make the iframe even more hidden.

For all of the above techniques to work, the JOBS_PAGE_URL variable
in the plugins must be set to the page that actually delivers the
cookies. For Kenexa and Brassring sites, this is generally the page
that has the 'Search Openings' link.

3. Resumator

4. Jobvite

Many times the jobs are listed within an iframe. The value of 
iframe['src'] is used as the basis for constructing links to
jobs::

 iframe['src']=
 http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qG19Vfwv&jvresize=http://www.percussion.com/web_resources/www.percussion.com/jobvite/FrameResize.html
 
The jvurlargs variable used in jvGoToPage() is set within the 
page itself as a global variable and has a value similar to::

  ?c=qG19Vfwv&jvprefix=http%3a%2f%2fwww.percussion.com&jvresize=http%3a%2f%2fwww.percussion.com%2fweb_resources%2fwww.percussion.com%2fjobvite%2fFrameResize.html

This value breaks down to::

  c        = qG19Vfwv
  jvprefix = http%3a%2f%2fwww.percussion.com
  jvresize = http%3a%2f%2fwww.percussion.com%2fweb_resources%2fwww.percussion.com%2fjobvite%2fFrameResize.html

The script needs to extract jvurlargs from the JavaScript source in order
to build proper job links.

The window.location.href value in jvGoToPage is equivalent to the value of 
the src attribute of the iframe containing the joblist::

  function jvGoToPage(page, arg, jobId, argList)
  {
      var l = window.location.href;
      var p = l.indexOf('?');

      if (p != -1)            
          l = l.substring(0, p); 
      
      l += jvurlargs + '&page=' + escape(page);

      if (arg && arg.length)
          l += '&arg=' + escape(arg);

      if (jobId && jobId.length)
          l += '&j=' + jobId;

      if (argList)
          l += argList;

      window.location.href = l;
  } 

For each job, jvGoToPage() is called with the page and jobId 
variables set as in the following example::

  jvGoToPage('Job Description','','otjDVfw4')

The variable 'l' gets constructed as follows as control
passes through jvGoToPage()::

  # l = window.location.href
  http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qG19Vfwv&jvresize=http://www.percussion.com/web_resources/www.percussion.com/jobvite/FrameResize.html

  # l = l.substring(0, '?')
  http://hire.jobvite.com/CompanyJobs/Careers.aspx 

  # l += jvurlargs + '&page' + escape(page)
  http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qG19Vfwv&jvprefix=http%3a%2f%2fwww.percussion.com&jvresize=http%3a%2f%2fwww.percussion.com%2fweb_resources%2fwww.percussion.com%2fjobvite%2fFrameResize.html&page=Job%20Description

  # l += '&j' + jobId
  http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=qG19Vfwv&jvprefix=http%3a%2f%2fwww.percussion.com&jvresize=http%3a%2f%2fwww.percussion.com%2fweb_resources%2fwww.percussion.com%2fjobvite%2fFrameResize.html&page=Job%20Description&j=otjDVfw4

5. PeopleAdmin

One of the versions of PeopleAdmin use a POST to retrieve the 
job description. Below is an example of the request sent by a
browser to retrieve the job information::

  https://colby-sawyer.simplehire.com/applicants/Central

  POST /applicants/Central HTTP/1.1
  Host: colby-sawyer.simplehire.com
  User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
  Accept-Language: en-us,en;q=0.5
  Accept-Encoding: gzip,deflate
  Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
  Keep-Alive: 115
  Connection: keep-alive
  Referer: https://colby-sawyer.simplehire.com/applicants/jsp/shared/search/SearchResults.jsp?time=1297883842492
  Cookie: JSESSIONID=9F8BE9F177578A495C872F89C7F6D943.node1
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 182
  windowTimestamp=PA_1297883838758&delegateParameter=applicantPostingSearchDelegate&actionParameter=getJobDetail&functionalityTableName=8192&rowId=137224&c=TXyNky1YAQUps1CK5dgy5g%3D%3D


  HTTP/1.1 200 OK
  Cache-Control: no-store, no-cache, must-revalidate, max-age=0
  Pragma: no-cache
  Content-Length: 527
  Content-Type: text/html;charset=ISO-8859-1
  Expires: -1
  Last-Modified: Wednesday, February 16, 2011 1:26:03 PM CST
  Server: Microsoft-IIS/7.5
  X-Powered-By: Servlet 2.4; JBoss-4.0.2 (build: CVSTag=JBoss_4_0_2 date=200505022023)/Tomcat-5.5
  Date: Wed, 16 Feb 2011 19:26:03 GMT
  ----------------------------------------------------------
  https://colby-sawyer.simplehire.com/applicants/jsp/shared/position/JobDetails.jsp?time=1297884363836

  GET /applicants/jsp/shared/position/JobDetails.jsp?time=1297884363836 HTTP/1.1
  Host: colby-sawyer.simplehire.com
  User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
  Accept-Language: en-us,en;q=0.5
  Accept-Encoding: gzip,deflate
  Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
  Keep-Alive: 115
  Connection: keep-alive
  Referer: https://colby-sawyer.simplehire.com/applicants/Central
  Cookie: JSESSIONID=9F8BE9F177578A495C872F89C7F6D943.node1

  HTTP/1.1 200 OK
  Content-Type: text/html;charset=ISO-8859-1
  Server: Microsoft-IIS/7.5
  X-Powered-By: Servlet 2.4; JBoss-4.0.2 (build: CVSTag=JBoss_4_0_2 date=200505022023)/Tomcat-5.5
  Date: Wed, 16 Feb 2011 19:26:03 GMT
  Content-Length: 17905
  ----------------------------------------------------------

The first POST request uses the URL https://colby-sawyer.simplehire.com/applicants/Central 
and a message body containing::

  windowTimestamp=PA_1297883838758&delegateParameter=applicantPostingSearchDelegate&actionParameter=getJobDetail&functionalityTableName=8192&rowId=137222&c=GvGk8%2BN%2FIpFhZjpaBacKPw%3D%3D

The message body of this POST request contains the following keys and values::

  windowTimestamp               PA_1297883838758
  delegateParameter             applicantPostingSearchDelegate
  actionParameter               getJobDetail
  functionalityTableName        8192
  rowId                         137222
  c                             GvGk8+N/IpFhZjpaBacKPw==

In order to build a link to this job posting on the front-end an
HTML form must be used. The form used on the actual job site is
shown below::

  <form name="link_8192_137224_0_0" method="POST" onsubmit="return checkEarlyFormSubmission(document.link_8192_137224_0_0.delegateParameter)" action="/applicants/Central">
    <input type="hidden" name="windowTimestamp" value="PA_1297883788898" />
    <input type="hidden" name="delegateParameter" value="applicantPostingSearchDelegate" />
    <input type="hidden" name="actionParameter" value="getJobDetail" />
    <input type="hidden" name="functionalityTableName" value="8192" />
    <input type="hidden" name="rowId" value="137224" />
    <input type="hidden" name="c" value="UFdC/Z7rpqmf2HfZuIThjQ==" />
    <div align="left">
      <a href="javascript:void(0);/* 137224 */" onclick="javascript: if(checkWindowTimestamp('PA_1297883788898') &amp;&amp; clickCheck()){  document.link_8192_137224_0_0.submit(); } return false;" class="commandLinkSmall">View</a>
    </div>
  </form>

A modified version of this form will work assuming your browser
doesn't have any leftover cookies from an ealier session with the
target site. The following form is the same as the previous except
that the action label now contains the full URL, the javascript
has been removed and a submit button labeled 'Job Description' has 
replaced the javascript link button::

  <html>
    <form name="link_8192_137224_0_0" method="POST" action="https://colby-sawyer.simplehire.com/applicants/Central">
      <input type="hidden" name="windowTimestamp" value="PA_1297883788898" />
      <input type="hidden" name="delegateParameter" value="applicantPostingSearchDelegate" />
      <input type="hidden" name="actionParameter" value="getJobDetail" />
      <input type="hidden" name="functionalityTableName" value="8192" />
      <input type="hidden" name="rowId" value="137224" />
      <input type="hidden" name="c" value="UFdC/Z7rpqmf2HfZuIThjQ==" />
      <div align="left">
        <input type='submit' value='Job Description'>
      </div>
    </form>
  </html>

The form still works even if the c and windowTimestamp fields are left out. In
fact for the link to work in Neekanee, the c field must be left out::

  <html>
    <form name="link_8192_137224_0_0" method="POST" action="https://colby-sawyer.simplehire.com/applicants/Central">
      <input type="hidden" name="delegateParameter" value="applicantPostingSearchDelegate" />
      <input type="hidden" name="actionParameter" value="getJobDetail" />
      <input type="hidden" name="functionalityTableName" value="8192" />
      <input type="hidden" name="rowId" value="137224" />
      <div align="left">
        <input type='submit' value='Job Description'>
      </div>
    </form>
  </html>

These forms require the user to click on a button named 'Job Description' in
order to visit the link containing the job description. To replace the button
with a text link, javascript needs to be used as in the original form::

  <html>
    <form name="job_0" method="POST" action="https://colby-sawyer.simplehire.com/applicants/Central">
      <input type="hidden" name="delegateParameter" value="applicantPostingSearchDelegate" />
      <input type="hidden" name="actionParameter" value="getJobDetail" />
      <input type="hidden" name="functionalityTableName" value="8192" />
      <input type="hidden" name="rowId" value="137224" />
      <div align="left">
        <a href="javascript:void(0);" onclick="javascript: { document.job_0.submit(); }">View</a>
      </div>
    </form>
  </html>

In order for the front-end to be able to build this form, the plugins must save 
the information used to construct the form. The plugins can save the form key-value
pairs by URL encoding them and saving the result into the data field of a Job
class. This is done by saving the form fields into a dictionary and then URL encoding
the dictionary.  The frontend can then take the urlencoded string and convert it back 
into a form when it is listing jobs for a company.

In the plugins, the function extract_form_fields() is used to convert the fields
in the form into a dictionary. The dictionary is then converted into URL encoded
form using urllib.urlencode().

On the frontend, the PHP function parse_str() is used to convert the key-value 
pairs from a URL encode string into an associate array. From there, the items in 
the associative array are used to build a form. Below is an example::

  <html>
    <form name="job_0" method="POST" action="https://colby-sawyer.simplehire.com/applicants/Central">

  <?php
      $str = 'windowTimestamp=PA_1297883838758&delegateParameter=applicantPostingSearchDelegate&actionParameter=getJobDetail&functionalityTableName=8192&rowId=137222&c=GvGk8%2BN%2FIpFhZjpaBacKPw%3D%3D';
      parse_str($str, $res);

      foreach ($res as $key => $value) {
          printf("<input type='hidden' name='" . $key . "' value='" . $value . "' />");
      }
  ?>

      <div align="left">
        <a href="javascript:void(0);" onclick="javascript: { document.job_0.submit(); }">View</a>
      </div>
    </form>
  </html>

Gotchas
=======
In some cases the <!DOCTYPE> tag in HTML will cause BeautifulSoup to parse
the HTML incorrectly. The fix is to chop off this tag and re-soupify::

    s = soupify(webcli.get(url))
    s = soupify(s.text[s.text.find('<html'):])

Look at ravemobilesafety as an example.

Geoparsing/Geocoding
====================
Yahoo Placemaker
Google Maps

Database Interaction
====================

Backend
=======

When creating the database for the first time, you must use the utf8 
character set. Otherwise MySQL will default to latin1 which will not
be able to store characters in some of the job descriptions.

On MySQL 5.1 this means using the command::

  CREATE DATABASE neekanee_solr CHARACTER SET utf8;

Note that on MySQL 5.1 the utf8 implementation can only store up 
to 3 bytes, even though it should go up to 4. MySQL 5.5 fixes this
with the utf8mb4 character set::

  CREATE DATABASE neekanee_solr CHARACTER SET utf8mb4

Frontend
========
Neekanee URL query parameters

Basic query parameters

         q | job search string
       loc | location string (eg. "boston, ma")
       lat | latitude
       lng | longitutde
    radius | location radius in miles


Refined search parameters

       tld | top-level domain (eg. "com", "net", "org") 
   company | company name (eg. "ViaSat")
    rating | 1-to-5 star company rating
     award | company has won one-or-more employer awards
      size | size of company 
     title | job title
