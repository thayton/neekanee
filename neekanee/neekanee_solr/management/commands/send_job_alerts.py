import sys

from django.http import QueryDict
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from django.template import Context

from neekanee_solr.models import *
from neekanee_solr.pysolr import Results, Solr
from neekanee_solr.solr_query_builder import *
from neekanee_solr.views import SearchResults
from neekanee_solr.linkup import LinkUp, LinkUpResults

ITEMS_PER_PAGE = 10

class Command(BaseCommand):
    help = 'Send job alerts to users'

    def handle(self, *args, **options):
        for job_alert in JobAlert.objects.all():
            if not job_alert.active:
                continue

            print '%s query=%s' % (job_alert.user.email, job_alert.query)

            jobs = self.jobs_for_job_alert(job_alert)
            if len(jobs) == 0:
                continue

            # Generate sponsored job ads
            query_dict = QueryDict(job_alert.query)
            linkup = LinkUp()
            response = linkup.search('127.0.0.1', query_dict.get('q', None), query_dict.get('loc', None), query_dict.get('company', None))
            sponsored_listings = LinkUpResults(response).sponsored_listings

#            plaintext = get_template('email.txt')
            htmly     = get_template('account/job_alerts_email.html')
            ctx = Context({'jobs': jobs, 'job_alert': job_alert, 'sponsored_listings': sponsored_listings})

            for email_address in job_alert.user.emailaddress_set.all():
                if email_address.primary and email_address.verified:
                    subject, from_email, to = 'Neekanee Job Alert', 'jobalert@neekanee.com', email_address.email
                    text_content = 'This is an important message.'
                    html_content = htmly.render(ctx)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    print 'Sent job alert email to ', to

            for job_result in jobs:
                job = Job.objects.get(pk=int(job_result['id']))
                job_already_alerted = JobAlreadyAlerted(job=job, alert=job_alert, user=job_alert.user)
                job_already_alerted.save()

    def jobs_for_job_alert(self, job_alert):
        pageno = 1
        jobs = []

        query_builder = SOLRJobSearchQueryBuilder(ITEMS_PER_PAGE)

        #
        # Build up our list of jobs until we reach ITEMS_PER_PAGE jobs.
        #
        while True:
            query_dict = QueryDict(job_alert.query)
            query_dict = query_dict.copy()
            query_dict['page'] = pageno
            query = query_builder.build_query(query_dict)

            conn = Solr('http://127.0.0.1:8983/solr/')
            results = SearchResults(conn.search(**query))

            #
            # Go through each job and remove the ones for which we've already 
            # sent alerts to this user.
            #
            # Also exclude jobs with url_data set since they will get implemented
            # as forms and we can't style them as links in emails
            #
            for job_result in results.docs:
                if len(job_result['url_data']) > 0:
                    continue

                job = Job.objects.get(pk=int(job_result['id']))
                try:
                    job_alert.user.jobalreadyalerted_set.get(alert=job_alert, job=job, user=job_alert.user)
                except JobAlreadyAlerted.DoesNotExist:
                    jobs.append(job_result)

                npages = (results.hits + ITEMS_PER_PAGE - 1)/ ITEMS_PER_PAGE

            if pageno >= npages or len(jobs) >= ITEMS_PER_PAGE:
                break

            pageno += 1

        return jobs[:ITEMS_PER_PAGE]
