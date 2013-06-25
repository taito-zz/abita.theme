from abita.theme.browser.interfaces import IRecentBlogViewlet
from abita.theme.browser.viewlet import RecentBlogViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class RecentBlogViewletTestCase(IntegrationTestCase):
    """TestCase for RecentBlogViewlet"""

    def test_subclass(self):
        from abita.theme.browser.viewlet import BaseRecentViewlet as Base
        self.assertTrue(issubclass(RecentBlogViewlet, Base))
        from abita.theme.browser.interfaces import IBaseRecentViewlet as Base
        self.assertTrue(issubclass(IRecentBlogViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(RecentBlogViewlet)
        self.assertTrue(verifyObject(IRecentBlogViewlet, instance))

    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    def test__brain(self, IAdapter):
        from Products.ATContentTypes.interfaces.news import IATNewsItem
        instance = self.create_viewlet(RecentBlogViewlet)
        instance._path = mock.Mock(return_value='PATH')
        self.assertIsNotNone(instance._brain())
        IAdapter().get_brain.assert_called_with(IATNewsItem, path='PATH', sort_on='effective', sort_order='descending', Language='en')
