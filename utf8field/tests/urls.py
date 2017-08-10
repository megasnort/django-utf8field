from django.conf.urls import include, url
from django.contrib import admin

from dev_example.views import test_view

admin.autodiscover()

urlpatterns = [
    url(r'^$', test_view),
    url(r'^admin/', include(admin.site.urls)),
]