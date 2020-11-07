
from videopath.apps.common.test_utils import BaseTestCase
from videopath.apps.payments.models import PendingSubscription

# Uses the standard django frame testing client
class TestCase(BaseTestCase):

    def setup(self):
        self.create_user()

    def test_creation(self):
    	subs = PendingSubscription.objects.create(user=self.user)
        self.assertIsNotNone(subs)