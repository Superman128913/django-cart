# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    # Auth routes - login / register
    path("", include("apps.cart.urls")),  # Cart
    path("", include("apps.authentication.urls")),
    path("", include("apps.home.urls")),             # UI Kits Html files
    path('captcha/', include("captcha.urls")),
    path('helpdesk/', include('helpdesk.urls')),
    path('admin/clearcache/', include('clearcache.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
