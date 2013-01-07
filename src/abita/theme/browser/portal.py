from Products.CMFCore.interfaces._content import ISiteRoot
from abita.theme.browser.interfaces import IAbitaThemeLayer
from five import grok


class View(grok.View):

    grok.context(ISiteRoot)
    grok.layer(IAbitaThemeLayer)
    grok.require('zope2.View')
    grok.name('abita-view')
