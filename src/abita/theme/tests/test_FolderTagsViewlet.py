# -*- coding: utf-8 -*-
from abita.theme.browser.interfaces import IFolderTagsViewlet
from abita.theme.browser.viewlet import FolderTagsViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class FolderTagsViewletTestCase(IntegrationTestCase):
    """TestCase for FolderTagsViewlet"""

    def test_subclass(self):
        from abita.theme.browser.viewlet import KeywordsViewlet as Base
        self.assertTrue(issubclass(FolderTagsViewlet, Base))
        from abita.theme.browser.interfaces import IKeywordsViewlet as Base
        self.assertTrue(issubclass(IFolderTagsViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(FolderTagsViewlet)
        self.assertTrue(verifyObject(IFolderTagsViewlet, instance))

    def test_categories(self):
        instance = self.create_viewlet(FolderTagsViewlet)
        instance.context.Subject = mock.Mock(return_value=('Äää', 'Ööö'))
        self.assertEqual(instance.categories(), [{
            'title': 'Äää',
            'url': 'http://nohost/plone?Subject=Äää',
        }, {
            'title': 'Ööö',
            'url': 'http://nohost/plone?Subject=Ööö',
        }])
