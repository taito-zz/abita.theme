from abita.theme.tests.base import IntegrationTestCase

import mock


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    @mock.patch('abita.theme.upgrades.reimport_profile')
    def test_reimport_viewlets(self, reimport_profile):
        from abita.theme.upgrades import reimport_viewlets
        reimport_viewlets(self.portal)
        reimport_profile.assert_called_with(self.portal, 'profile-abita.theme:default', 'viewlets')

    @mock.patch('abita.theme.upgrades.reimport_profile')
    def test_reimport_typeinfo(self, reimport_profile):
        from abita.theme.upgrades import reimport_typeinfo
        reimport_typeinfo(self.portal)
        reimport_profile.assert_called_with(self.portal, 'profile-abita.theme:default', 'typeinfo')

    def test_show_path_bar(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.abovecontent"
        storage.setHidden(manager, "Plone Default", ('plone.path_bar',))
        storage.setHidden(manager, "Plone Classic Theme", ('plone.path_bar',))
        storage.setHidden(manager, "Sunburst Theme", ('plone.path_bar',))
        self.assertIn('plone.path_bar', storage.getHidden(manager, "Plone Default"))
        self.assertIn('plone.path_bar', storage.getHidden(manager, "Plone Classic Theme"))
        self.assertIn('plone.path_bar', storage.getHidden(manager, "Sunburst Theme"))

        from abita.theme.upgrades import show_path_bar
        show_path_bar(self.portal)

        self.assertEqual(storage.getHidden(manager, "Plone Default"), ())
        self.assertEqual(storage.getHidden(manager, "Plone Classic Theme"), ())
        self.assertEqual(storage.getHidden(manager, "Sunburst Theme"), ())
