# -*- coding: utf-8 -*-
from abita.theme.browser.interfaces import IServiceTextViewlet
from abita.theme.browser.viewlet import ServiceTextViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class ServiceTextViewletTestCase(IntegrationTestCase):
    """TestCase for ServiceTextViewlet"""

    def test_subclass(self):
        from collective.base.viewlet import Viewlet as Base
        self.assertTrue(issubclass(ServiceTextViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IServiceTextViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(ServiceTextViewlet)
        self.assertTrue(verifyObject(IServiceTextViewlet, instance))

    def test_available(self):
        instance = self.create_viewlet(ServiceTextViewlet)
        instance.text = mock.Mock()
        self.assertTrue(instance.available())

        instance.text.return_value = None
        self.assertFalse(instance.available())

    def test_text(self):
        view = mock.Mock()
        view.doc().CookedBody.return_value = 'TEXT'
        instance = self.create_viewlet(ServiceTextViewlet, view=view)
        self.assertEqual(instance.text(), 'TEXT')
