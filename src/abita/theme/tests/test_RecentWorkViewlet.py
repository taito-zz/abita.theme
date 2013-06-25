from abita.theme.browser.interfaces import IRecentWorkViewlet
from abita.theme.browser.viewlet import RecentWorkViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class RecentWorkViewletTestCase(IntegrationTestCase):
    """TestCase for RecentWorkViewlet"""

    def test_subclass(self):
        from abita.theme.browser.viewlet import BaseRecentViewlet as Base
        self.assertTrue(issubclass(RecentWorkViewlet, Base))
        from abita.theme.browser.interfaces import IBaseRecentViewlet as Base
        self.assertTrue(issubclass(IRecentWorkViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(RecentWorkViewlet)
        self.assertTrue(verifyObject(IRecentWorkViewlet, instance))

    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    def test__brain(self, IAdapter):
        from Products.ATContentTypes.interfaces.event import IATEvent
        instance = self.create_viewlet(RecentWorkViewlet)
        instance._path = mock.Mock(return_value='PATH')
        self.assertIsNotNone(instance._brain())
        IAdapter().get_brain.assert_called_with(IATEvent, path='PATH', sort_on='end', sort_order='descending', Language='en')
