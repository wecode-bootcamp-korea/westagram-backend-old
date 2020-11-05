## path 정보
user/regist			= 회원가입(POST)
user/login			= 로그인(POST)
posting/resist			= 포스팅 등록(POST)
posting/show_all_posts		= 전체 포스팅 보기(GET)
posting/add_comment		= comment 추가(POST)
posting/show_all_comments	= 전체 comment 보기(GET)

To do Tomorrow
1. join을 이용하여 FK 값을 실제 값으로(user_id면 user의 name) 제공하도록 수정
   target : ShowAllComments, ShowAllPosts
