from django.conf.urls import include, url
from django.contrib import admin

from dev_example.views import TestCreate

admin.autodiscover()

urlpatterns = [
    url(r'^$', TestCreate.as_view()),
    url(r'^admin/', include(admin.site.urls)),
]