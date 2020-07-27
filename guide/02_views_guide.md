# 사용하지 않는 코드 및 주석 제거

django app 을 생성하고 `views.py`를 여셨나요?

```python
from django.shortcuts import render

# Create your views here.
```

열자 마자 보이는 위와 같은 코드는 프로젝트에서 사용하지 않습니다.
사용하지 않는 모듈이나 클래스를 import 하지 않도록 제거해주세요.
사용하지 않는 주석도 모두 제거해주세요.
