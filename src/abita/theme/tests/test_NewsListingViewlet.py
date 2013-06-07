# -*- coding: utf-8 -*-
from abita.theme.browser.interfaces import INewsListingViewlet
from abita.theme.browser.viewlet import NewsListingViewlet
from abita.theme.tests.base import IntegrationTestCase

import mock


class NewsListingViewletTestCase(IntegrationTestCase):
    """TestCase for NewsListingViewlet"""

    def test_subclass(self):
        from collective.base.viewlet import Viewlet as Base
        self.assertTrue(issubclass(NewsListingViewlet, Base))
        from collective.base.interfaces import IViewlet as Base
        self.assertTrue(issubclass(INewsListingViewlet, Base))

    def test_verifyObject(self):
        from zope.interface.verify import verifyObject
        instance = self.create_viewlet(NewsListingViewlet)
        self.assertTrue(verifyObject(INewsListingViewlet, instance))

    def test_available(self):
        instance = self.create_viewlet(NewsListingViewlet)
        instance.news = mock.Mock()
        self.assertTrue(instance.available())

        instance.news.return_value = None
        self.assertFalse(instance.available())

    @mock.patch('abita.theme.browser.viewlet.IAdapter')
    @mock.patch('Products.CMFPlone.browser.ploneview.Plone.toLocalizedTime', mock.Mock(return_value='LOCALIZED_TIME'))
    def test_news(self, IAdapter):
        view = mock.Mock()
        view.subject.return_value = ('Äää',)
        item = mock.Mock()
        item.Title.return_value = 'TITLE'
        item.Description.return_value = 'DESCRIPTION'
        item.id = 'ID'
        item.getURL.return_value = 'URL'
        item.effective.asdatetime().date().isoformat.return_value = '2013-06-07'
        IAdapter().get_content_listing.return_value = [item]
        instance = self.create_viewlet(NewsListingViewlet, view=view)
        instance._subjects = mock.Mock(return_value='SUBJECTS')
        self.assertEqual(instance.news(), [{
            'title': 'TITLE',
            'description': 'DESCRIPTION',
            'id': 'ID',
            'url': 'URL',
            'date': 'LOCALIZED_TIME',
            'datetime': '2013-06-07',
            'subjects': 'SUBJECTS',
        }])

    @mock.patch('abita.theme.browser.viewlet.aq_parent')
    def test__subjects(self, aq_parent):
        instance = self.create_viewlet(NewsListingViewlet)
        aq_parent().absolute_url.return_value = 'URL'
        item = mock.Mock()
        item.Subject.return_value = ('Äää', 'Ööö')
        self.assertEqual(instance._subjects(item), [{
            'title': 'Äää',
            'url': 'URL?Subject=Äää',
        }, {
            'title': 'Ööö',
            'url': 'URL?Subject=Ööö',
        }])
