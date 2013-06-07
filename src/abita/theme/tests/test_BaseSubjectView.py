# -*- coding: utf-8 -*-
from abita.theme.browser.interfaces import IBaseSubjectView
from abita.theme.browser.view import BaseSubjectView
from abita.theme.tests.base import IntegrationTestCase

import mock


class BaseSubjectViewTestCase(IntegrationTestCase):
    """TestCase for BaseSubjectView"""

    def test_subclass(self):
        from collective.base.view import BaseView as Base
        self.assertTrue(issubclass(BaseSubjectView, Base))
        from collective.base.interfaces import IBaseView as Base
        self.assertTrue(issubclass(IBaseSubjectView, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_view(BaseSubjectView)
        self.assertTrue(verifyObject(IBaseSubjectView, instance))

    def test_subject(self):
        instance = self.create_view(BaseSubjectView)
        instance.request.form = {'Subject': 'SUBJECT'}
        self.assertEqual(instance.subject(), 'SUBJECT')

    @mock.patch('abita.theme.browser.view.IAdapter')
    def test_doc(self, IAdapter):
        from Products.ATContentTypes.interfaces.document import IATDocument
        instance = self.create_view(BaseSubjectView)
        instance.subject = mock.Mock(return_value='SUBJECT')
        self.assertIsNotNone(instance.doc())
        IAdapter().get_object.assert_called_with(IATDocument, depth=1, Subject='SUBJECT')

    def test_title(self):
        instance = self.create_view(BaseSubjectView)
        self.portal.Title = mock.Mock(return_value='PORTAL_TITLE')
        self.assertEqual(instance.title(), 'PORTAL_TITLE')

        instance.doc = mock.Mock()
        instance.doc().Title.return_value = 'DOC_TITLE'
        self.assertEqual(instance.title(), 'DOC_TITLE')

    def test_description(self):
        instance = self.create_view(BaseSubjectView)
        self.portal.Description = mock.Mock(return_value='PORTAL_DESCRIPTION')
        self.assertEqual(instance.description(), 'PORTAL_DESCRIPTION')

        instance.doc = mock.Mock()
        instance.doc().Description.return_value = 'DOC_DESCRIPTION'
        self.assertEqual(instance.description(), 'DOC_DESCRIPTION')
