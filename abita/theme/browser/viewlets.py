from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.viewlets.common import PathBarViewlet
from plone.app.layout.viewlets.common import ViewletBase
from sll.policy.browser.interfaces import ITopPageFeed
from zope.component import getMultiAdapter


class FeedViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlets/feed.pt')

    def feeds(
        self,
        limit=3,
        object_provides=IATDocument.__identifier__,
        path=None,
        Subject=None,
        ):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        query = {
            'object_provides': object_provides,
            'sort_on': 'modified', 
            'sort_order': 'reverse',
            'sort_limit': limit,
        }
        if path is not None:
            query['path'] = path
        if Subject is not None:
            query['Subject'] = Subject
        res = catalog(query)[:limit]
        ploneview = getMultiAdapter(
            (context, self.request),
            name=u'plone'
        )
        items = [
            {
                'title': item.Title(),
                'url': item.getURL(),
                # 'parent': aq_parent(item.getObject()).Title(),
                # 'parent_url': aq_parent(item.getObject()).absolute_url(),
                'description': self.description(item),
                # 'object': item.getObject(),
                # 'image': self.image(item),
                'date': ploneview.toLocalizedTime(item.ModificationDate()),
            } for item in IContentListing(res)
        ]
        return items

    def description(self, item):
        desc = item.Description()
        length = 200
        if len(desc) > length:
            ploneview = getMultiAdapter(
                (self.context, self.request),
                name=u'plone'
            )
            desc = ploneview.cropText(desc, length)
        return desc

class BusinessTopicsViewlet(FeedViewlet):

    title = 'Business Topics'

    def items(self):
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        path = {
                'query': '{0}/topics'.format(portal_state.navigation_root_path()),
                'depth': 1,
        }
        return self.feeds(limit=1, path=path)


class NewsViewlet(FeedViewlet):

    title = 'News'

    def items(self):
        return self.feeds(
            object_provides=IATNewsItem.__identifier__
        )


class ApplicationReleasesViewlet(FeedViewlet):

    title = 'Application Releases'

    def items(self):
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        path = {
                'query': '{0}/applications'.format(portal_state.navigation_root_path()),
                'depth': 1,
        }
        return self.feeds(limit=1, path=path)


# class NewsEventsFeedViewlet(ViewletBase):
#     index = ViewPageTemplateFile('viewlets/news_events_feed.pt')


# class SimpleFeedViewlet(ViewletBase):
#     index = ViewPageTemplateFile('viewlets/simple_feed.pt')

#     def feeds(self, identifier, limit=3):
#         context = aq_inner(self.context)
#         catalog = getToolByName(context, 'portal_catalog')
#         query = {
#             'object_provides': identifier,
#             'sort_on': 'modified', 
#             'sort_order': 'reverse',
#             'sort_limit': limit,
#         }
#         res = catalog(query)[:limit]
#         ploneview = getMultiAdapter(
#             (context, self.request),
#             name=u'plone'
#         )
#         items = [
#             {
#                 'title': item.Title(),
#                 'url': item.getURL(),
#                 'parent': aq_parent(item.getObject()).Title(),
#                 'parent_url': aq_parent(item.getObject()).absolute_url(),
#                 'date': ploneview.toLocalizedTime(item.ModificationDate()),
#             } for item in IContentListing(res)
#         ]
#         return items


# class NewsFeedViewlet(SimpleFeedViewlet):

#     def items(self):
#         return self.feeds(IATNewsItem.__identifier__)


# class EventsFeedViewlet(SimpleFeedViewlet):

#     def items(self):
#         return self.feeds(IATEvent.__identifier__)


# class FooterInfoViewlet(ViewletBase):
#     index = ViewPageTemplateFile('viewlets/footer_info.pt')

#     def items(self):
#         context = aq_inner(self.context)
#         portal_state = getMultiAdapter((context, self.request), name="plone_portal_state")
#         catalog = getToolByName(context, 'portal_catalog')
#         query = {
#             'object_provides': IATDocument.__identifier__,
#             'path': {
#                 'query': '{0}/info'.format(portal_state.navigation_root_path()),
#             },
#             'sort_on': 'getObjPositionInParent',
#         }
#         res = catalog(query)
#         if res:
#             width = '{0}'.format(100 / len(res))[:2]
#             self.width = 'width: {0}%'.format(width)
#             items = [
#                 {
#                     'title': item.Title(),
#                     'url': item.getURL(),
#                     'description': item.Description(),
#                     'text': item.getObject().CookedBody(),
#                 } for item in IContentListing(res)
#             ]
#             return items


# class FooterSubfoldersViewlet(ViewletBase):
#     index = ViewPageTemplateFile('viewlets/footer_subfolders.pt')

#     def items(self):
#         context = aq_inner(self.context)
#         portal_state = getMultiAdapter((context, self.request), name="plone_portal_state")
#         catalog = getToolByName(context, 'portal_catalog')
#         query = {
#             'object_provides': IATFolder.__identifier__,
#             'path': {
#                 'query': portal_state.navigation_root_path(),
#                 'depth': 1,
#             },
#             'sort_on': 'getObjPositionInParent',
#         }
#         res = [brain for brain in catalog(query) if not brain.exclude_from_nav]
#         ploneview = getMultiAdapter(
#             (context, self.request),
#             name=u'plone'
#         )
#         items = [
#             {
#                 'title': item.Title(),
#                 'url': item.getURL(),
#                 'description': item.Description(),
#                 'subfolders': self.subfolders(item, catalog, ploneview),
#             } for item in IContentListing(res)
#         ]
#         return items

#     def subfolders(self, item, catalog, ploneview):
#         query = {
#             'object_provides': IATFolder.__identifier__,
#             'path': {
#                 'query': item.getPath(),
#                 'depth': 1,
#             },
#             'sort_on': 'getObjPositionInParent',
#         }
#         res = catalog(query)
#         items = [
#             {
#                 'title': item.Title(),
#                 'url': item.getURL(),
#                 'description': item.Description(),
#             } for item in IContentListing(res)
#         ]
#         return items