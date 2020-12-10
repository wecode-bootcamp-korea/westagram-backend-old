#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls    import path
from user.views import UserView,SigninView,FollowsView

urlpatterns = [
    path('/signup', UserView.as_view()),
    path('/signin', SigninView.as_view()),
    path('/follow/<int:user_pk>',FollowsView.as_view()),
]
