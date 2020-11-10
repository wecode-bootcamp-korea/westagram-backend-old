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