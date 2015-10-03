from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'clrms.views.home', name='home'),
    #url(r'^clrms/', include('clrms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/update', 'clrms.account.views.update'),
    url(r'^update-comp', 'clrms.account.views.update_comp'),
    url(r'^$', 'clrms.account.views.home'),
    url(r'^love', 'clrms.account.views.love'),
    url(r'^login-check/', 'clrms.account.views.login_check'),
    url(r'^signup-check/', 'clrms.account.views.signup_check'),
    url(r'^welcome', 'clrms.account.views.welcome'),
    url(r'^search', 'clrms.account.views.search'),
    url(r'^overview', 'clrms.account.views.overview'),
    url(r'^complaint', 'clrms.account.views.complaint'),
    url(r'^LabSelect', 'clrms.account.views.LabSelect'),
    url(r'^ComplaintForm', 'clrms.account.views.ComplaintForm'),
    url(r'^Complaint-Final/', 'clrms.account.views.complaint_final'),
    url(r'^Complaint-Send/', 'clrms.account.views.complaint_send'),
    url(r'^Thank-You', 'clrms.account.views.thank_you'),
    url(r'^range', 'clrms.account.views.range'),
    url(r'^lab/', 'clrms.account.views.Dlab'),
    url(r'^stats/', 'clrms.account.views.stats'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.MEDIA_URL + 'images/favicon.ico'))

    #url(r'^Lab/Database-Lab', 'clrms.account.views.Dlab',{'lab_choice':''}),
    #url(r'^Foss-Lab', 'clrms.account.views.Dlab',{'lab_choice':2}),
    #url(r'^Networks-Lab', 'clrms.account.views.Dlab',{'lab_choice':3}),
    #url(r'^Project-Lab', 'clrms.account.views.Dlab',{'lab_choice':4}),
)
