import unittest
from twitter.twitter import TwitterUser
from mock import Mock

def create_mock_twitter_user():
	user = Mock()
	user.name = 'Alex Siqueira'
	user.id = 14147108
	return user

class TestTwitterUser(unittest.TestCase):

	def test_isonline(self):
		user = TwitterUser('alegomes')

	def test_name_retrieval(self):
		user = create_mock_twitter_user()
		self.assertEqual('Alex Siqueira', user.name)

	def test_id_retrieval(self):
		user = create_mock_twitter_user()
		self.assertEqual(14147108, user.id)


if __name__ == '__main__':
    unittest.main()
