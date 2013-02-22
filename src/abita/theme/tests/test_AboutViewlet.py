# -*- coding: utf-8 -*-
from abita.theme.tests.base import IntegrationTestCase
from zope.publisher.browser import TestRequest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class TestAboutViewlet(IntegrationTestCase):
    """Test for AboutViewlet"""

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.about = self.portal[self.portal.invokeFactory('Folder', 'about', title="Äböut",
            description="Description of Äböut")]
        self.about.reindexObject()

    def create_doc(self):
        en = self.about[self.about.invokeFactory('Document', 'en',
            title='English', description="Description of English", text="<p>Text of English</p>")]
        en.reindexObject()

    def create_instance(self):
        from abita.theme.browser.viewlet import AboutViewlet
        return AboutViewlet(self.portal, TestRequest(), manager=None, view=None)

    def test_obj__folder(self):
        instance = self.create_instance()
        self.assertIsNone(instance.obj)

    def test_obj__doc(self):
        instance = self.create_instance()
        self.create_doc()
        self.assertEqual(instance.obj, self.portal['about']['en'])

    def test_title__folder(self):
        instance = self.create_instance()
        self.assertEqual(instance.title, 'Äböut')

    def test_title__doc(self):
        instance = self.create_instance()
        self.create_doc()
        self.assertEqual(instance.title, 'English')

    def test_description__folder(self):
        instance = self.create_instance()
        self.assertEqual(instance.description, 'Description of Äböut')

    def test_description__doc(self):
        instance = self.create_instance()
        self.create_doc()
        self.assertEqual(instance.description, 'Description of English')

    def test_text__folder(self):
        instance = self.create_instance()
        self.assertIsNone(instance.text)

    def test_text__doc(self):
        instance = self.create_instance()
        self.create_doc()
        self.assertEqual(instance.text, '<p>Text of English</p>')
