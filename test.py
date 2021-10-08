import unittest
from user import User, VKUser

TOKEN = ''
ID = ''


class TestVk(unittest.TestCase):
    def setUp(self):
        self.Vk = VKUser(token=TOKEN, id=ID)

    def test_get_res(self):
        res = self.Vk.get_my_info()
        self.assertEqual(len(res), 11)

    def tearDown(self):
        print("testing over")


class TestUser(unittest.TestCase):
    def setUp(self):
        self.User = User(id_user=ID, token=TOKEN, age_from=20, age_to=30)

    def test_search_people(self):
        res = self.User.search_people()
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 10)

    def test_top_photo(self):
        people = self.User.search_people()
        res = self.User.top_photo(people)
        self.assertEqual(len(res), 10)
        self.assertIsInstance(res, list)

    def test_select_id(self):
        self.assertIsInstance(self.User.select_id(), list)

    def tearDown(self):
        print("testing over")


if __name__ == '__main__':
    unittest.main()

