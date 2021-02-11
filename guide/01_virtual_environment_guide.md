
위스타그램 프로젝트를 위해 새로운 가상 환경을 설정하겠습니다. 

# 1. 가상 환경

### 1. 가상환경 생성
가상 환경은 프로젝트마다 하나씩 생성하시는 것을 추천드립니다. 매 프로젝트마다 필요한 환경이 조금씩 다를 수 있기 때문입니다. `westagram`이라는 이름의 가상 환경을 생성하겠습니다. 이 환경에는 파이썬 3.8버전이 설치될 것입니다.
```
conda create -n westagram python=3.8
```
### 2. 가상환경 활성화
가상환경의 목록을 먼저 확인하신 후, `westagram`이라는 가상 환경이 잘 생성되었다면, 가상환경을 활성화합니다
```
conda activate westagram
```


# 2. Django 설치

실행시킨 가상환경 `westagram`에 django를 설치하겠습니다.

```bash
pip install django
```
자, 이제 westagram 프로젝트를 위한 가상환경 설정이 완료 되었습니다. 장고를 설치했다면 프로젝트를 생성해볼까요? 이름은 `project_westagram` 이 좋겠네요.

```bash
django-admin startproject project_westagram
```

그렇다면 다음으로 기초 django 설정을 해보겠습니다. 다음 가이드를 계속 진행해주세요 😃