# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from includes_test_app import views


admin.autodiscover()


urlpatterns = [

    url( r'^admin/', admin.site.urls ),  # eg host/project_x/admin/

    url( r'^info/$', views.info, name='info_url' ),

    url( r'^just_internal/$', views.just_internal, name='internal_url' ),

    url( r'^external_include/$', views.external, name='external_url' ),

    url( r'^proxy/$', views.proxy, name='proxy_url' ),
    url( r'^proxy/(?P<slug>.*)/$', views.proxy, name='proxy_url' ),

    url( r'^bul_search/$', views.bul_search, name='bul_search_url' ),

    url( r'^$', RedirectView.as_view(pattern_name='info_url') ),

    ]
