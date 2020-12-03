#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls    import path
from user.views import UserView

urlpatterns = [
    path('', UserView.as_view())
]
