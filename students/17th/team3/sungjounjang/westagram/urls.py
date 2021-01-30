from django.urls import path, include

import user

urlpatterns = [
    path('account/', include(user.urls))
]
