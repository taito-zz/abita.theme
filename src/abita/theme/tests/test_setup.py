from Products.CMFCore.utils import getToolByName
from abita.theme.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_package_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('abita.theme'))

    def test_browserlayer(self):
        from abita.theme.browser.interfaces import IAbitaThemeLayer
        from plone.browserlayer import utils
        self.assertIn(IAbitaThemeLayer, utils.registered_layers())

    def test_cssregistry__abita_theme_main(self):
        resource = getToolByName(self.portal, 'portal_css').getResource('++resource++abita.theme/css/main.css')
        self.assertTrue(resource.getApplyPrefix())
        self.assertFalse(resource.getAuthenticated())
        self.assertEqual(resource.getCompression(), 'safe')
        self.assertEqual(resource.getConditionalcomment(), '')
        self.assertTrue(resource.getCookable())
        self.assertTrue(resource.getEnabled())
        self.assertEqual(resource.getExpression(), '')
        self.assertEqual(resource.getMedia(), 'screen')
        self.assertEqual(resource.getRel(), 'stylesheet')
        self.assertEqual(resource.getRendering(), 'link')
        self.assertIsNone(resource.getTitle())

    def test_cssregistry__abita_theme_extra__applyPrefix(self):
        resource = getToolByName(self.portal, 'portal_css').getResource('++resource++abita.theme/css/extra.css')
        self.assertTrue(resource.getApplyPrefix())
        self.assertFalse(resource.getAuthenticated())
        self.assertEqual(resource.getCompression(), 'safe')
        self.assertEqual(resource.getConditionalcomment(), '')
        self.assertTrue(resource.getCookable())
        self.assertTrue(resource.getEnabled())
        self.assertEqual(resource.getExpression(), '')
        self.assertEqual(resource.getMedia(), 'screen')
        self.assertEqual(resource.getRel(), 'stylesheet')
        self.assertEqual(resource.getRendering(), 'link')
        self.assertIsNone(resource.getTitle())

    def test_metadata__dependency__abita_basetheme(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('abita.basetheme'))

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-abita.theme:default'), u'4')

    def test_types__Folder(self):
        types = getToolByName(self.portal, 'portal_types')
        methods = ['work-history']
        for method in methods:
            self.assertIn(method, types.getTypeInfo('Folder').getProperty('view_methods'))

    def test_viewlets__hidden__plone_portalheader(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.portalheader"
        skinname = "*"
        self.assertIn(u'plone.searchbox', storage.getHidden(manager, skinname))

    def test_viewlets__hidden__plone_portalfooter(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.portalfooter"
        skinname = "*"
        for viewlet in (
            u'plone.colophon',
            u'plone.site_actions'):
            self.assertIn(viewlet, storage.getHidden(manager, skinname))

    def test_uninstall_package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.theme'])
        self.assertFalse(installer.isProductInstalled('abita.theme'))

    def test_uninstall_browserlayer(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.theme'])
        from abita.theme.browser.interfaces import IAbitaThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(IAbitaThemeLayer, utils.registered_layers())

    def test_uninstall_cssregistry__abita_theme_main(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.theme'])
        self.assertIsNone(getToolByName(self.portal, 'portal_css').getResource('++resource++abita.theme/css/main.css'))

    def test_uninstall_cssregistry__abita_theme_extra(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.theme'])
        self.assertIsNone(getToolByName(self.portal, 'portal_css').getResource('++resource++abita.theme/css/extra.css'))
