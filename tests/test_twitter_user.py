import pytest
import warnings
from modules.twitter_user import TwitterUser
from modules.twitter_api import TwitterAPI

class TestTwitterUser():

    def test_name_retrieval(self):
        user = TwitterUser('siqueiralex')
        assert 'Alex Siqueira' == user.name
        assert  '52126452' == user.id

    def test_account_existance(self):
        user = TwitterUser('')
        assert user.existence == False

	# time consuming
    def test_false_account(self):
        user = TwitterUser('mrinasilv')
        assert user.existence == False
