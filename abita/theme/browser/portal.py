from five import grok
from abita.theme.browser.interfaces import IAbitaThemeLayer
from Products.CMFCore.interfaces._content import ISiteRoot


class View(grok.View):

    grok.context(ISiteRoot)
    grok.layer(IAbitaThemeLayer)
    grok.require('zope2.View')
    grok.name('abita-view')
