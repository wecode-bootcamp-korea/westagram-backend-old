
가상 환경 정보
miniconda with python 3.8
django==3.1.5
django-cors-headers==3.7.0
mysqlclient==2.0.3
bcrypt==3.2.0
pyjwt==2.0.1

admin, auth는 구현 예정. django 내장은 주석 처리했습니다.

회원 가입 후 사용자 정보가 저장되는 테이블: users
column name
- email    : 회원가입시 필수 항목. 로그인시 사용할 id. 최대 100 글자.
- password : 사용자가 로그인시 사용할 비밀번호. 필수 항목. 최소 8 글자 이상. 최대 100 글자.
- account  : 사용자가 로그인시 사용할 수 있는 id. 최대 20 글자.
- phone_number : 사용자가 로그인시 사용할 수 있는 전화번호. 최대 12글자('-' 못 넣도록).
- created_at   : 회원가입 일시. 자동 추가.
- updated_at   : 회원 정보를 마지막으로 수정한 일시. 자동 추가 및 수정.

수정 필요
email, password validation 정규식
password 길이 - 암호화를 언제 하는지?
phone_number에 '-' 못 넣도록 하기.

엔드포인트

1. localhost/user/signup
POST. email과 password가 필수입니다.

2. localhost/user/login
POST. email, account, phone_number 셋 중 하나와 password가 필수입니다.
