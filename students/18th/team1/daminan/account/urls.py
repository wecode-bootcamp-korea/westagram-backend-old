from django.urls import path
from .views      import SignupView, LoginView, FollowView

urlpatterns = [
    path('/user', SignupView.as_view()),
    path('/login', LoginView.as_view()),    
    path('/follow', FollowView.as_view()),    

]
'''Error가 아니라 django의 권장사항. 하지만 패턴 컨벤션에는 위 사항이 맞다.'''
