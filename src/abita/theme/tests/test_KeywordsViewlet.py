# -*- coding: utf-8 -*-
from abita.theme.browser.interfaces import IKeywordsViewlet
from abita.theme.browser.viewlet import KeywordsViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class KeywordsViewletTestCase(IntegrationTestCase):
    """TestCase for KeywordsViewlet"""

    def test_subclass(self):
        from collective.base.viewlet import Viewlet as Base
        self.assertTrue(issubclass(KeywordsViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IKeywordsViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(KeywordsViewlet)
        self.assertTrue(verifyObject(IKeywordsViewlet, instance))

    def test_available(self):
        instance = self.create_viewlet(KeywordsViewlet)
        instance.categories = mock.Mock()
        self.assertTrue(instance.available())

    @mock.patch('abita.theme.browser.viewlet.aq_parent')
    @mock.patch('abita.theme.browser.viewlet.IATEvent')
    def test_categories(self, IATEvent, aq_parent):
        instance = self.create_viewlet(KeywordsViewlet)
        aq_parent().absolute_url.return_value = 'URL'
        instance.context.Subject = mock.Mock(return_value=('Äää', 'Ööö'))
        self.assertEqual(instance.categories(), [{
            'title': 'Äää',
            'url': 'URL?Subject=Äää',
        }, {
            'title': 'Ööö',
            'url': 'URL?Subject=Ööö',
        }])
