# from Acquisition import aq_inner
# from Products.ATContentTypes.interfaces.document import IATDocument
# from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from abita.adapter.interfaces import IBaseAdapter
from abita.theme.browser.interfaces import IAbitaThemeLayer
# from abita.theme.browser.interfaces import ITopViewletManager
from five import grok
# from plone.app.contentlisting.interfaces import IContentListing
# from plone.app.layout.viewlets.common import ViewletBase
# from zope.component import getMultiAdapter


grok.templatedir('viewlets')


# class FeedViewlet(ViewletBase):
#     id = None
#     index = ViewPageTemplateFile('viewlets/feed.pt')

#     def feeds(
#         self,
#         limit=0,
#         object_provides=IATDocument.__identifier__,
#         path=None,
#         Subject=None):
#         context = aq_inner(self.context)
#         catalog = getToolByName(context, 'portal_catalog')
#         query = {
#             'object_provides': object_provides,
#             'sort_on': 'modified',
#             'sort_order': 'reverse',
#         }
#         if path is not None:
#             query['path'] = path
#         if Subject is not None:
#             query['Subject'] = Subject
#         brains = []
#         if limit:
#             query['sort_limit'] = limit
#             brains = catalog(query)[:limit]
#         items = catalog(query) if not brains else brains
#         ploneview = getMultiAdapter(
#             (context, self.request), name=u'plone')
#         if items:
#             items = [{
#                 'title': item.Title(),
#                 'url': item.getURL(),
#                 'description': self.description(item),
#                 'date': ploneview.toLocalizedTime(item.ModificationDate()),
#             } for item in IContentListing(items)]
#         return items

#     def description(self, item):
#         desc = item.Description()
#         length = 200
#         if len(desc) > length:
#             ploneview = getMultiAdapter(
#                 (self.context, self.request), name=u'plone')
#             desc = ploneview.cropText(desc, length)
#         return desc

#     def title(self):
#         if self.context.get(self.id):
#             return self.context[self.id].Title()

#     def url(self):
#         if self.context.get(self.id):
#             return self.context[self.id].absolute_url()


# class ApplicationReleasesViewlet(FeedViewlet):

#     id = 'applications'

#     def items(self):
#         portal_state = getMultiAdapter(
#             (self.context, self.request),
#             name=u'plone_portal_state'
#         )
#         path = {
#                 'query': '{0}/applications'.format(portal_state.navigation_root_path()),
#                 'depth': 1,
#         }
#         return self.feeds(limit=20, path=path)


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
    def obj(self):
        adapter = IBaseAdapter(self.context[self.name])
        return adapter.get_object(depth=1)

    def title(self):
        return self.context[self.name].Title()

    def description(self):
        return self.context[self.name].Description()

    def text(self):
        if self.obj:
            return self.obj.CookedBody()


# class AboutViewlet(BaseViewlet):
#     name = 'about'
#     grok.name('abita.theme.about')


class ContactViewlet(BaseViewlet):
    name = 'contact'
    grok.name('abita.theme.contact')
