from neekanee_solr.models import *
from django.contrib import admin

class VacationAccrualInline(admin.TabularInline):
    model = VacationAccrual
    extra = 1

class SickLeaveAccrualInline(admin.TabularInline):
    model = SickLeaveAccrual
    extra = 1

class CompanyLocationInline(admin.TabularInline):
    model = CompanyLocation
    extra = 1

class CompanyLocationPhotoInline(admin.TabularInline):
    model = CompanyLocationPhoto
    extra = 1

class CompanyWorkLifePhotoInline(admin.TabularInline):
    model = CompanyWorkLifePhoto
    extra = 1

class CompanyTagInline(admin.TabularInline):
    model = CompanyTag
    extra = 1

class CompanyLocationTagInline(admin.TabularInline):
    model = CompanyLocationTag
    extra = 1

class CompanyAwardInline(admin.TabularInline):
    model = CompanyAward
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'job_count', 'tags' )
    inlines = [ VacationAccrualInline, SickLeaveAccrualInline, CompanyTagInline, CompanyLocationInline, CompanyAwardInline, CompanyWorkLifePhotoInline ]

    # So we can sort the companies table based on number of jobs at each company
    def queryset(self, request):
        qs = super(CompanyAdmin, self).queryset(request)
        qs = qs.annotate(models.Count('job'))
        return qs

    def job_count(self, model_instance):
        return model_instance.job_set.count()
    job_count.admin_order_field = 'job__count'

class CompanyLocationAdmin(admin.ModelAdmin):
    search_fields = ['company__name']
    inlines = [ CompanyLocationTagInline, CompanyLocationPhotoInline ]

admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyLocation, CompanyLocationAdmin)
admin.site.register(CompanySize)
admin.site.register(Award)
admin.site.register(CompanyAward)
admin.site.register(Tag)
admin.site.register(CompanyTag)
admin.site.register(CompanyLocationTag)
admin.site.register(JobAlert)
