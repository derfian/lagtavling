from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tavling.views',
    # Examples:
    url(r'^$',                              'index'),
    url(r'^tavling/(?P<tavling_id>\d+)/$',  'tavling'),
    url(r'^ekipage/(?P<ekipage_id>\d+)/$',  'ekipage'),
    url(r'^lag/(?P<lag_id>\d+)/$',          'lag'),
)

urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
