from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from abita.adapter.interfaces import IBaseAdapter
from abita.theme.browser.interfaces import IAbitaThemeLayer
from five import grok


grok.templatedir('viewlets')


class TopViewletManager(grok.ViewletManager):
    """Viewlet manager for top page"""
    grok.context(IPloneSiteRoot)
    grok.layer(IAbitaThemeLayer)
    grok.name('abita.theme.top.manager')


class BaseViewlet(grok.Viewlet):
    """Base class for viewlet"""
    name = ''
    grok.baseclass()
    grok.context(IPloneSiteRoot)
    grok.layer(IAbitaThemeLayer)
    grok.require('zope2.View')
    grok.template('top')
    grok.viewletmanager(TopViewletManager)

    @property
    def folder(self):
        return self.context.get(self.name)

    @property
    def obj(self):
        adapter = IBaseAdapter(self.folder)
        return adapter.get_object(depth=1)

    @property
    def title(self):
        if self.obj:
            return self.obj.Title()
        return self.folder.Title()

    @property
    def description(self):
        if self.obj:
            return self.obj.Description()
        return self.folder.Description()

    @property
    def text(self):
        if self.obj:
            return self.obj.CookedBody()


class AboutViewlet(BaseViewlet):
    name = 'about'
    grok.name('abita.theme.about')
