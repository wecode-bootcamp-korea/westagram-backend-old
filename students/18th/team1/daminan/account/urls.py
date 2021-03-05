from django.urls import path
from .views      import SignupView, LoginView

urlpatterns = [
    path('user', SignupView.as_view()),
    path('login', LoginView.as_view()),    
]
'''urls.py 슬래시 위치 확인
(urls.w002) your url pattern '/user' has a route beginning with a '/'. remove this slash as it is unnecessary. if this pattern is targeted in an include(), ensure the include() pattern has a trailing '/'.
에러 나서 / 사용 위와 같이 함.'''
