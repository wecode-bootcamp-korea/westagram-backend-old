# westagram-backend

## 초기 세팅 및 진행 방법
- 원하는 directory 이동 후 해당 repo를 clone 받아주세요.
- master 브랜치를 기준으로 `feature/본인이름` 브랜치를 만들어주세요. (ex. `feature/joonsikyang`)
- 새롭게 생성한 브랜치로 이동후 `students > 기수` 폴더에 본인 이름의 폴더를 만들어주세요. 
(ex. `students` > `4th` > `joonsikyang` 폴더 생성)
- 해당 폴더에 기존에 작업했던 프로젝트 메인 디렉토리와 앱 디렉토리, `manage.py` 파일들을 전 복사 붙여넣기 해주세요.
- 이렇게 폴더 및 파일 구조 세팅이 완료되면 작업을 진행합니다.
- 작업 중간 중간 commit 잘 남기고, 완료 시 origin master로 push 후 PR 까지 완료해주세요.
- 리뷰 내용은 반영해서 코드 수정하고 다시 push 해주세요.
- 해당 branch가 merge되면 미션 완료입니다.

## 리뷰 코멘트를 반영한 뒤 진행 방법
- 멘토님들이 남긴 코멘트를 잘 읽고 브랜치에서 코드를 수정해주세요.
- 수정 하신 후 다시 add, commit, push 해주세요.
- 수정이 완료된 코멘트에는 `Resolve conversation` 버튼을 눌러주세요.

## 필수 구현 항목
- [User] 회원가입 엔드포인트(SignUp): 
    - 회원가입 로직 작성
    - url 연결
    - 이메일이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 반환

- [User] 로그인 엔드포인트(SignIn):
    - 로그인 로직 작성
    - url 연결
    - 로그인 성공시 {"message": "SUCCESS"}, status code 200 return
    - 실패시 {"message": "INVALID_USER"}, status code 401 에러 return

## 보너스 구현 사항
- [Posting] 특정 유저의 게시물에 댓글 달기 엔드포인트
    - 유저 아이디, 댓글 내용, 최초 댓글 단 시간, 수정 시간 포함될 것
- [Posting] 특정 유저의 게시물에 '좋아요' 누르기 엔드포인트 
- [Posting] 게시물 올리기
- [User] 회원가입시 email, password validation
    - email: '@' 포함하였는지 검사
    - password: 5글자 이상인지 검사
- [User] 다른 회원 follow 하기 엔드포인트

## 위코드 파이썬 코딩 컨벤션
- Import 순서
    1. Python 모듈
    2. Django 모듈
    3. 내가 만든 모듈

    ```python
    import json
    # 간격 한 줄 
    from django.db import models
    # 간격 한 줄
    from user.models    import User
    from product.models import Drink        
    ```

- Code Align
    - `import` 를 기준으로 정렬해주세요
    - `Class`나 `Function` 내부에서 선언하는 변수들의 경우 `=`을 기준으로 정렬해줍니다.
    ```python
    from user.models    import User
    from product.models import Drink

        class Product(models.Model):
            product_code    = models.CharField(max_length=100, null=True)
            name            = models.CharField(max_length=50, null=True)
            price           = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    ```
- 보다 자세한 규칙은 노션에서 확인해주세요
