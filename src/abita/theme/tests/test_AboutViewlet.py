from abita.basetheme.browser.interfaces import IAboutViewlet
from abita.theme.browser.viewlet import AboutViewlet
from abita.theme.tests.base import IntegrationTestCase


class AboutViewletTestCase(IntegrationTestCase):
    """TestCase for AboutViewlet"""

    def test_subclass(self):
        from abita.basetheme.browser.viewlet import BaseDocumentViewlet as Base
        self.assertTrue(issubclass(AboutViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(AboutViewlet)
        self.assertTrue(verifyObject(IAboutViewlet, instance))

    def test_obj(self):
        instance = self.create_viewlet(AboutViewlet)
        self.assertIsNone(instance.obj())
