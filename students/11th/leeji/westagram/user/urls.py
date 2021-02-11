from django.urls  import path
from .views       import Sign_UP_View,Sign_In_View

urlpatterns = [
    path('/up',Sign_UP_View.as_view() ),
    path('/in',Sign_In_View.as_view() ),
]