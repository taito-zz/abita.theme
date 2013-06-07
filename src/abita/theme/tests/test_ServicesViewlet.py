# -*- coding: utf-8 -*-
from abita.theme.browser.interfaces import IServicesViewlet
from abita.theme.browser.viewlet import ServicesViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class ServicesViewletTestCase(IntegrationTestCase):
    """TestCase for ServicesViewlet"""

    def test_subclass(self):
        from collective.base.viewlet import Viewlet as Base
        self.assertTrue(issubclass(ServicesViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IServicesViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(ServicesViewlet)
        self.assertTrue(verifyObject(IServicesViewlet, instance))

    def test_available(self):
        instance = self.create_viewlet(ServicesViewlet)
        instance.services = mock.Mock()
        self.assertTrue(instance.available())

        instance.services.return_value = None
        self.assertFalse(instance.available())

    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    def test_services(self, IAdapter):
        item = mock.Mock()
        item.Subject.return_value = ('Äää',)
        item.Title.return_value = 'TITLE'
        item.Description.return_value = 'DESCRIPTION'
        item.id = 'ID'
        IAdapter().get_content_listing.return_value = [item]
        instance = self.create_viewlet(ServicesViewlet)
        self.assertEqual(instance.services(), [{
            'title': 'TITLE',
            'description': 'DESCRIPTION',
            'id': 'ID',
            'url': 'http://nohost/plone?Subject=Äää',
        }])
