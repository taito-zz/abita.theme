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

    def test_available(self):
        instance = self.create_viewlet(RecentServiceViewlet)
        instance.items = mock.Mock()
        self.assertTrue(instance.available())

        instance.items.return_value = None
        self.assertFalse(instance.available())

    @mock.patch('abita.theme.browser.viewlet.IEventAdapter')
    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    def test_items(self, IAdapter, IEventAdapter):
        view = mock.Mock()
        view.subject.return_value = ('Äää')
        item = mock.Mock()
        item.contactName = 'CONTACT'
        item.eventUrl = 'EVENT_URL'
        item.Description.return_value = 'DESCRIPITON'
        item.location = 'LOCATION'
        item.Title.return_value = 'TITLE'
        item.getURL.return_value = 'URL'
        IEventAdapter().year.return_value = '2013'
        instance = self.create_viewlet(RecentServiceViewlet, view=view)
        instance._subjects = mock.Mock(return_value='SUBJECTS')
        IAdapter().get_content_listing.return_value = [item]
        self.assertEqual(instance.items(), [{
            'client': 'CONTACT',
            'client_url': 'EVENT_URL',
            'description': 'DESCRIPITON',
            'location': 'LOCATION',
            'subjects': 'SUBJECTS',
            'title': 'TITLE',
            'url': 'URL',
            'year': '2013',
        }])
