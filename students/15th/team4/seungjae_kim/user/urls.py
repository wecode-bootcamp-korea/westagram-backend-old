#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls    import path
from user.views import UserView,SigninView

urlpatterns = [
    path('/signup', UserView.as_view()),
    path('/signin', SigninView.as_view())
]
