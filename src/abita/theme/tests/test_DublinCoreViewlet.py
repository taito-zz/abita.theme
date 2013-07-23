from abita.theme.browser.viewlet import DublinCoreViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class DublinCoreViewletTestCase(IntegrationTestCase):
    """TestCase for DublinCoreViewlet"""

    def test_subclass(self):
        from abita.basetheme.browser.viewlet import BaseDocumentViewlet
        from plone.app.layout.viewlets.common import DublinCoreViewlet as Base
        self.assertTrue(issubclass(DublinCoreViewlet, (Base, BaseDocumentViewlet)))

    def test_update(self):
        instance = self.create_viewlet(DublinCoreViewlet)
        instance.update()
        self.assertEqual(instance.metatags, [])

        obj = mock.Mock()
        obj.Description.return_value = 'DESCRIPTION'
        instance.obj = mock.Mock(return_value=obj)
        instance.update()
        self.assertEqual(instance.metatags, [('description', 'DESCRIPTION')])
