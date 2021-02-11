
위스타그램 프로젝트를 위해 수정해야할 django settings에 대해 알아보겠습니다.
`project_westagram/settings.py` 를 열어주세요.

# 1. 기본 설정

### 1. INSTALLED_APPS에서 사용하지 않을 앱 삭제
- INSTALLED_APPS라는 속성에서 `django.contirb.admin`과 `django.contrib.auth`는 사용하지 않습니다. 주석처리 해주세요.
```python
INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    ...
]
```

- MIDDLEWARE에서도 `csrf`관련 요소와 `auth`관련 요소를 주석처리 해주세요.
```python
MIDDLEWARE = [
    ...
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
]
```

CORS에 관련된 내용은 추후에 좀 더 자세하게 배우겠습니다. 

# 2. 외부 접속 허용

`Django`를 설치해둔 가상환경을 실행시켜 주세요.
```bash
conda activate westagram
```
그 다음 플러그인을 설치해주세요.
```bash
pip install django-cors-headers
```

### 1. ALLOWED_HOSTS 추가

내 서버에 다른 컴퓨터가 접속을 시도합니다. 무분별한 접속을 차단하기 위해 우리는 특정 아이피 주소를 가진 접속만을 허용하기 위해서 `ALLED_HOSTS`를 수정합니다. 보통 허용하고자 하는 아이피 주소만을 입력하지만, 프로젝트 진행시 여러 아이피 주소를 허용해야 하기에 `*`을 이용하여 모두 허용해줍니다.

```python
ALLOWED_HOSTS = ['*']
```

### 2. INSTALLED_APPS에 corsheaders 추가

CORS에 대해 공부해보세요. 프론트엔드와 통신을 할 때에는 서로 다른 port로 접속을 시도합니다. 이를 허용해주기 위하여 `INSTALLED_APPS`에 기존 설정 사항 아래에 `corsheaders`를 추가해줍니다.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]
```

### 3. middleware 추가

```python
    MIDDLEWARE = [
	...
		'corsheaders.middleware.CorsMiddleware',
]
```

### 4. CORS 관련 허용 사항 추가
설정 파일 제일 아래에 다음 코드를 추가해주세요.
```
##CORS
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
```

자, 이제 westagram 프로젝트를 위한 기본 설정이 완료 되었습니다. westagram을 위한 첫 앱을 생성해보세요! 회원가입, 로그인 등 회원을 관리할 앱을 생성하실 것이므로 앱 이름은 `user` 혹은 `account`를 추천드립니다.

어떻게 만들죠?

```bash
python manage.py startapp user
```
앱을 만드신 뒤에는 다음 가이드를 확인해주세요.
