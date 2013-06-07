# -*- coding: utf-8 -*-
from abita.theme.browser.interfaces import IRecentServiceViewlet
from abita.theme.browser.viewlet import RecentServiceViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class RecentServiceViewletTestCase(IntegrationTestCase):
    """TestCase for RecentServiceViewlet"""

    def test_subclass(self):
        from abita.theme.browser.viewlet import RecentWorkViewlet as Base
        self.assertTrue(issubclass(RecentServiceViewlet, Base))
        from abita.theme.browser.interfaces import IRecentWorkViewlet as Base
        self.assertTrue(issubclass(IRecentServiceViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(RecentServiceViewlet)
        self.assertTrue(verifyObject(IRecentServiceViewlet, instance))

    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    def test__brain__0(self, IAdapter):
        from Products.ATContentTypes.interfaces.event import IATEvent
        view = mock.Mock()
        view.subject.return_value = ('Äää',)
        instance = self.create_viewlet(RecentServiceViewlet, view=view)
        instance._path = mock.Mock(return_value='PATH')
        self.assertIsNotNone(instance._brain())
        IAdapter().get_brain.assert_called_with(IATEvent, path='PATH', sort_on='end', sort_order='descending', Subject=('Äää',))

    @mock.patch('abita.theme.browser.viewlet.RecentWorkViewlet._brain')
    def test__brain__1(self, _brain):
        view = mock.Mock()
        instance = self.create_viewlet(RecentServiceViewlet, view=view)
        instance.view.subject.return_value = None
        instance = self.create_viewlet(RecentServiceViewlet, view=view)
        self.assertIsNotNone(instance._brain())
        self.assertTrue(_brain.called)
