"""
Definition of urls for Penguinness.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.contrib import admin


import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact', app.views.contact, name='contact'),
    url(r'^emailsuccess', app.views.emailsuccess, name='emailsuccess'),
    url(r'^Team', app.views.team, name='team'),
    url(r'^links', app.views.links, name='links'),

    url(r'thebook',app.views.thebook,name='thebook'),
    url(r'Dive_compare',app.views.divecompare,name='divecompare'),
    url(r'DiveData/',app.views.divedata,name='divedata'),
    url(r'Learn_more/',app.views.learnmore,name='learnmore'),
    url(r'info/', app.views.learnsearch,name='learnsearch'),

    
    url(r'spec/',app.views.specsearch,name='specsearch'),
    url(r'subgrp/',app.views.subgrp,name='subgrp'),
    url(r'subcats/',app.views.subcats,name='subcats'),
    url(r'cats/',app.views.cats,name='cats'), 
    
    #url(r'species/',app.values.species,name='species'),

    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
]
