from django.test import TestCase

class UserTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # 클래스 전체에서 사용되는 설정을 위해서 테스트 시작 때 한 번만 실행된다.
        # 테스트 메서드가 실행되면서 수정되거나 변경되지 않을 객체들을 이곳에서 생성한다.
        print("setUpTestData")
        pass
    
    def setUp(self):
        # 각각의 테스트 메서드가 실행될 때 마다 실행된다.
        # 테스트 중 내용이 변경될 수 있는 객체를 이곳에서 생성할 수 있다.
        # 모든 테스트 메서드는 막 생성된 (fresh) 한 오브젝트를 입력받게 된다.
        # TearDown 메서드는 베이스 클래스가 TestCase인데 DB삭제를 처리하기 때문에,
        # DB테스트에는 적합하지 않다.
        print("setUp")
        pass
    
    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)
    
    def test_false_is_true(self):
        print("Method: test_false_is_true")
        self.assertTrue(True)
    
    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_equals_two.")
        self.assertEqual(1 + 1, 2)

# 테스트를 실행시키는 법
# pm test (pm -> python manage.py)
# 현재 경로에서 test*.py 패턴을 만족하는 모든 파일을 찾은 후 테스트를 적합한 베이스 클래스를
# 이용해서 실행한다.
# pm test 를 실행시키면 ValueError: Missing staticssfiles manifest entry..
# 에러가 발생할 수 있다.
# 테스팅 도구가 기본적으로 collectstatic 을 실행하지 않고 storage 클래스를 사용하기?
# 때문이다. (manifest_strict) 를 참조.
# pm collectstatic 실행해서 해결하라.

# 테스트에 대해 더 많은 정보 출력하기
# pm test --verbosity2
# verbosity levels 는 0, 1, 2, 3 : 기본값 1

# 테스트의 일부만 실행하기
# TestCase 서브 클래스, 메서드 전체 경로를 지정한다.
# pm test user.tests
# pm test user.tests.test_models
# pm test user.tests.test_models.YourTestClass
# pm test user.tests.test_models.YourTestClass.YourTestMethod
















