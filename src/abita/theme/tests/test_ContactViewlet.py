from abita.theme.tests.base import IntegrationTestCase
from zope.publisher.browser import TestRequest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class TestCase(IntegrationTestCase):
    """TestCase for ContactViewlet"""

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.contact = self.portal[self.portal.invokeFactory('Folder', 'contact', title="Contact",
            description="Description of Contact")]
        self.contact.reindexObject()

    def create_doc(self):
        en = self.contact[self.contact.invokeFactory('Document', 'en',
            title='English', description="Description of English", text="<p>Text of English</p>")]
        en.reindexObject()

    def create_instance(self):
        from abita.theme.browser.viewlet import ContactViewlet
        return ContactViewlet(self.portal, TestRequest(), manager=None, view=None)

    def test_obj__folder(self):
        instance = self.create_instance()
        self.assertIsNone(instance.obj)

    def test_obj__doc(self):
        instance = self.create_instance()
        self.create_doc()
        self.assertEqual(instance.obj, self.portal['contact']['en'])

    def test_title__folder(self):
        instance = self.create_instance()
        self.assertEqual(instance.title, 'Contact')

    def test_title__doc(self):
        instance = self.create_instance()
        self.create_doc()
        self.assertEqual(instance.title, 'English')

    def test_description__folder(self):
        instance = self.create_instance()
        self.assertEqual(instance.description, 'Description of Contact')

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
