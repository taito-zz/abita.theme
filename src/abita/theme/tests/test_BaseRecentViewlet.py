# -*- coding: utf-8 -*-
from abita.theme.browser.interfaces import IBaseRecentViewlet
from abita.theme.browser.viewlet import BaseRecentViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class BaseRecentViewletTestCase(IntegrationTestCase):
    """TestCase for BaseRecentViewlet"""

    def test_subclass(self):
        from collective.base.viewlet import Viewlet as Base
        self.assertTrue(issubclass(BaseRecentViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(IBaseRecentViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(BaseRecentViewlet)
        self.assertTrue(verifyObject(IBaseRecentViewlet, instance))

    def test__path(self):
        instance = self.create_viewlet(BaseRecentViewlet)
        self.assertEqual(instance._path(), '/plone/')

    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    def test__subjects__0(self, IAdapter):
        instance = self.create_viewlet(BaseRecentViewlet)
        brain = mock.Mock()
        brain.Subject = ()
        IAdapter().get_brain().Title = 'ÄÄÄ'
        IAdapter().get_brain().Description = 'ÖÖÖ'
        IAdapter().get_brain().getURL.return_value = 'ÅÅÅ'
        self.assertEqual(instance._subjects(brain), [{
            'description': 'ÖÖÖ',
            'title': 'ÄÄÄ',
            'url': 'ÅÅÅ',
        }])

    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    def test__subjects__1(self, IAdapter):
        instance = self.create_viewlet(BaseRecentViewlet)
        brain = mock.Mock()
        brain.Subject = ()
        IAdapter().get_brain.return_value = None
        self.assertEqual(instance._subjects(brain), [])

    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    def test__subjects__2(self, IAdapter):
        instance = self.create_viewlet(BaseRecentViewlet)
        brain = mock.Mock()
        brain.Subject = ('Äää', 'Ööö')
        IAdapter().get_brain.return_value = None
        self.assertEqual(instance._subjects(brain), [{
            'description': None,
            'title': 'Äää',
            'url': None,
        }, {
            'description': None,
            'title': 'Ööö',
            'url': None,
        }])

    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    def test__subjects__3(self, IAdapter):
        instance = self.create_viewlet(BaseRecentViewlet)
        brain = mock.Mock()
        brain.Subject = ('Äää', 'Ööö')
        IAdapter().get_brain().Title = 'ÄÄÄ'
        IAdapter().get_brain().Description = 'ÖÖÖ'
        IAdapter().get_brain().getURL.return_value = 'ÅÅÅ'
        self.assertEqual(instance._subjects(brain), [{
            'description': 'ÖÖÖ',
            'title': 'ÄÄÄ',
            'url': 'ÅÅÅ',
        }, {
            'description': 'ÖÖÖ',
            'title': 'ÄÄÄ',
            'url': 'ÅÅÅ',
        }, {
            'description': 'ÖÖÖ',
            'title': 'ÄÄÄ',
            'url': 'ÅÅÅ',
        }])

    def test_item__0(self):
        instance = self.create_viewlet(BaseRecentViewlet)
        self.assertIsNone(instance.item())

    def test_item__1(self):
        instance = self.create_viewlet(BaseRecentViewlet)
        brain = mock.Mock()
        brain.Title = 'ÄÄÄ'
        brain.Description = 'ÖÖÖ'
        brain.getURL.return_value = 'ÅÅÅ'
        instance._subjects = mock.Mock(return_value=[])
        instance._brain = mock.Mock(return_value=brain)
        self.assertEqual(instance.item(), {
            'description': 'ÖÖÖ',
            'subjects': [],
            'title': 'ÄÄÄ',
            'url': 'ÅÅÅ',
        })

    def test_available__0(self):
        instance = self.create_viewlet(BaseRecentViewlet)
        instance._brain = mock.Mock(return_value=None)
        self.assertFalse(instance.available())

    def test_available__1(self):
        instance = self.create_viewlet(BaseRecentViewlet)
        instance._brain = mock.Mock()
        self.assertTrue(instance.available())

    def test_style_class(self):
        instance = self.create_viewlet(BaseRecentViewlet)
        instance.__name__ = 'aaa.bbb.ccc.ddd'
        self.assertEqual(instance.style_class(), 'ddd')
