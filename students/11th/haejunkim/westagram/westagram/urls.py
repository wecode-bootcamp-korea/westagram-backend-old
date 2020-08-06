from django.urls import(
    path, 
    include
)

urlpatterns = [
    path('user/', include('User.urls')),
    path('post/', include('Post.urls')),
]
