from django.conf.urls.defaults import *

import webhooks.views
from webhooks.models import WebHookRequest

# Uncomment the next two lines to enable the admin:
from django.contrib import admin


admin.autodiscover()
admin.site.register(WebHookRequest)

urlpatterns = patterns('',
    # Example:
    # (r'^plugin_repository/', include('plugin_repository.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^webhooks/$', webhooks.views.process_webhook),
)
