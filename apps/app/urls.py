# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.app.models import scrapperprofile
from django.urls import path, re_path
from apps.app import views

urlpatterns = [

    # The home page
    path('', views.dashboard, name='home'),
   # path('dashboard', views.dashboard, name='dashboard'),

    path('databasetable', views.databasetable, name='databasetable'),
    path('tableview', views.tableview, name='tableview'),
    path('scrapperpost', views.scrapperpost, name='scrapperpost'),

    path('profilesetting/<slug:pk>/', views.PersonUpdateView.as_view(), name='profilesetting'),

    path("api/scrapper/<int:id>", views.scrapperapi),
    path("api/allprofiles",views.scrapperprofileview),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
