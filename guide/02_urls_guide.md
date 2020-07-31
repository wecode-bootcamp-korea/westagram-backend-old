
# 사용하지 않는 코드 및 주석 제거

### urls.py
django project를 생성하고 `urls.py`를 여셨나요?

```python
"""
Some descriptions
"""
from django.contrib import admin ----- [1]

urlpatterns = [
    path('admin/', admin.site.urls), - [2]
]

```
열자 마자 보이는 위와 같은 코드 가운데에는 사용하지 않는 코드가 있습니다.
`admin`을 사용하지 않기 때문에 [1],[2] 코드를 제거해주세요

이제 django app을 생성하신 뒤 다음 가이드를 봐주세요.
