from Products.CMFCore.utils import getToolByName
from abita.theme.tests.base import IntegrationTestCase
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


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

    def test_catalog__index(self):
        from Products.PluginIndexes.FieldIndex.FieldIndex import FieldIndex
        catalog = getToolByName(self.portal, 'portal_catalog')
        self.assertIsInstance(catalog.Indexes['Language'], FieldIndex)

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
            setup.getVersionForProfile('profile-abita.theme:default'), u'6')

    def test_registry(self):
        self.assertEqual(getUtility(IRegistry)['abita.development.rate'], 10.0)
        self.assertEqual(getUtility(IRegistry)['abita.development.vat'], 0.0)

    def test_types__Folder(self):
        types = getToolByName(self.portal, 'portal_types')
        methods = ['work-history']
        for method in methods:
            self.assertIn(method, types.getTypeInfo('Folder').getProperty('view_methods'))

    def test_viewlets__hidden__collective_base_viewlet_manager_base(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "collective.base.viewlet-manager.base"
        skinname = "*"
        for viewlet in (
            u'abita.basetheme.viewlet.about',):
            self.assertIn(viewlet, storage.getHidden(manager, skinname))

    def test_viewlets__order__collective_base_viewlet_manager_base(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "collective.base.viewlet-manager.base"
        skinname = "*"
        for viewlet in (
            u'abita.theme.viewlet.about',
            u'abita.theme.viewlet.recent-work',
            u'abita.theme.viewlet.recent-contribution',
            u'abita.theme.viewlet.work-history',
            u'abita.theme.viewlet.work-history-event',
            u'abita.theme.viewlet.services',
            u'abita.theme.viewlet.service-text',
            u'abita.theme.viewlet.recent-service',
            u'abita.theme.viewlet.news-listing'):
            self.assertIn(viewlet, storage.getOrder(manager, skinname))

    def test_viewlets__order__plone_abovecontent(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.abovecontent"
        skinname = "*"
        for viewlet in (
            u'plone.path_bar', ):
            self.assertIn(viewlet, storage.getOrder(manager, skinname))

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
