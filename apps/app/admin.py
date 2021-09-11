# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(scrapperprofile)
class scrapperprofileAdmin(admin.ModelAdmin):

    list_display = [
        'profilelink', "uploaded_at" ,"scrapped_status","added_by"]