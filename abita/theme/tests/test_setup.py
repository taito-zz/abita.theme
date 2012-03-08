from abita.theme.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_is_abita_theme_installed(self):
        self.failUnless(self.installer.isProductInstalled('abita.theme'))

    def test_is_plone_app_theming_installed(self):
        self.failUnless(self.installer.isProductInstalled('plone.app.theming'))

    def test_uninstall(self):
        self.installer.uninstallProducts(['abita.theme'])
        self.failIf(self.installer.isProductInstalled('abita.theme'))

    def test_browserlayer(self):
        from abita.theme.browser.interfaces import IAbitaThemeLayer
        from plone.browserlayer import utils
        self.failUnless(IAbitaThemeLayer in utils.registered_layers())

    def test_css_registry_configured(self):
        css_resources = set(
            getToolByName(self.portal, 'portal_css').getResourceIds())

        self.failUnless(
            '++theme++abita.theme/css/style.css' in css_resources)

    # def test_js_registry_configured(self):
    #     js_resources = set(
    #         getToolByName(self.portal, 'portal_javascripts').getResourceIds())

    #     self.failUnless(
    #         '++theme++abita.theme/javascript/libs/modernizr.custom.js'
    #         in js_resources)
    #     self.failUnless(
    #         '++theme++abita.theme/javascript/libs/respond.min.js'
    #         in js_resources)


    def test_theme__enabled(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        from plone.app.theming.interfaces import IThemeSettings
        settings = registry.forInterface(IThemeSettings)
        self.assertTrue(settings.enabled)

    def test_theme__rules(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        from plone.app.theming.interfaces import IThemeSettings
        settings = registry.forInterface(IThemeSettings)
        self.assertEqual(
            settings.rules,
            "/++theme++abita.theme/rules.xml"
        )

    def test_theme__absolutePrefix(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        from plone.app.theming.interfaces import IThemeSettings
        settings = registry.forInterface(IThemeSettings)
        self.assertEqual(
            settings.absolutePrefix,
            "/++theme++abita.theme"
        )

    def test_doctype_configured(self):
        from plone.app.theming.interfaces import IThemeSettings
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility

        settings = getUtility(IRegistry).forInterface(IThemeSettings)
        self.assertEqual(settings.doctype, '<!doctype html>')
