
가상 환경 정보
miniconda with python 3.8
django==3.1.5
django-cors-headers==3.7.0

admin, auth는 구현 예정. django 내장은 주석 처리함.

회원 가입 후 사용자 정보가 저장되는 테이블: users
column name
- account  : 사용자가 로그인시 사용할 id. 최대 6글자.
- password : 사용자가 로그인시 사용할 비밀번호. 최대 8글자.
