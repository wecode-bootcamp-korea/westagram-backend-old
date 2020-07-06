# westagram-backend

> 디테일한 가이드는 guide 폴더에 있는 md 파일 내용을 확인해주세요.

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

## 필수 구현 항목
- [User] 회원가입 엔드포인트(SignUp): 
    - 회원가입 로직 작성
    - url 연결
    - 이미 가입한 회원인지 확인하여 적절한 에러메세지 반환 (ex. EXISTING_ACCOUNT)
- [User] 로그인 엔드포인트(SignIn):
    - 로그인 로직 작성
    - url 연결
    - 로그인시 계정이 틀렸거나 비밀번호가 틀렸을 때 적절한 에러메세지 반환 (ex. WRONG_PASSWORD) 

## 보너스 구현 사항
- [Posting] 특정 유저의 게시물에 댓글 달기 엔드포인트
- [Posting] 특정 유저의 게시물에 '좋아요' 누르기 엔드포인트 
- [User] 회원가입시 email, password validation
    - email: '@' 포함하였는지 검사
    - password: 5글자 이상인지 검사
- [User] 다른 회원 follow 하기 엔드포인트

