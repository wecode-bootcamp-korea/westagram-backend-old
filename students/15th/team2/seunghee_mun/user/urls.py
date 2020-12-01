from django.urls import path # 이것도 어디 sys에 django.http랑 같이 있겠지...?
from user.views import UserView # 같은 디렉토리에 있는 views.py 파일을 불러옴.

urlpatterns = [
	path('', UserView.as_view())
]
