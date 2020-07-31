
settings.py 를 모두 수정하셨다면 project/urls.py 파일을 열어주세요.

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
`admin`을 사용하지 않기 때문에 [1],[2] 코드를 제거해주세요.

django app을 생성하셨다면, [03_views.guid.md](https://github.com/wecode-bootcamp-korea/westagram-backend/blob/master/guide/03_views_guid.md) 파일을 확인해주세요.
