from Acquisition import aq_inner
from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter


class FeedViewlet(ViewletBase):
    id = None
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
        items = catalog(query)[:limit]
        ploneview = getMultiAdapter(
            (context, self.request),
            name=u'plone'
        )
        if items:
            items = [
                {
                    'title': item.Title(),
                    'url': item.getURL(),
                    'description': self.description(item),
                    'date': ploneview.toLocalizedTime(item.ModificationDate()),
                } for item in IContentListing(items)
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

    def title(self):
        if self.context.get(self.id):
            return self.context[self.id].Title()

    def url(self):
        if self.context.get(self.id):
            return self.context[self.id].absolute_url()

class BusinessTopicsViewlet(FeedViewlet):

    id = 'topics'

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

    id = 'news'

    def items(self):
        return self.feeds(
            object_provides=IATNewsItem.__identifier__
        )


class ApplicationReleasesViewlet(FeedViewlet):

    id = 'applications'

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
