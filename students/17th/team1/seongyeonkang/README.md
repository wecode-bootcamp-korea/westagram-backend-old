
가상 환경 정보
miniconda with python 3.8
django==3.1.5
django-cors-headers==3.7.0
mysqlclient==2.0.3

admin, auth는 구현 예정. django 내장은 주석 처리했습니다.

회원 가입 후 사용자 정보가 저장되는 테이블: users
column name
- email    : 회원가입시 필수 항목. 로그인시 사용할 id. 최대 30글자.
- password : 사용자가 로그인시 사용할 비밀번호. 필수 항목. 최소 8글자 이상.
- account  : 사용자가 로그인시 사용할 수 있는 id.
- phone_number : 사용자가 로그인시 사용할 수 있는 전화번호
- created_at   : 회원가입 일시. 자동 추가.
- updated_at   : 회원 정보를 마지막으로 수정한 일시. 자동 추가 및 수정.

지금은 email, password 관련 에러만 처리해둔 상태입니다.

엔드포인트
1. /user/signup
2. /user/login
지금 둘 다 POST만 있고 email과 password를 필수 키로 갖습니다.
