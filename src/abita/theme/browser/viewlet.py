from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from abita.theme import _
from abita.theme.browser.interfaces import IBaseRecentViewlet
from abita.theme.browser.interfaces import IRecentContributionViewlet
from abita.theme.browser.interfaces import IFolderTagsViewlet
from abita.theme.browser.interfaces import IKeywordsViewlet
from abita.theme.browser.interfaces import INewsListingViewlet
from abita.theme.browser.interfaces import IRecentBlogViewlet
from abita.theme.browser.interfaces import IRecentServiceViewlet
from abita.theme.browser.interfaces import IRecentWorkViewlet
from abita.theme.browser.interfaces import IServiceTextViewlet
from abita.theme.browser.interfaces import IServicesViewlet
from abita.theme.browser.interfaces import IWorkHistoryEventViewlet
from abita.theme.browser.interfaces import IWorkHistoryViewlet
from abita.theme.interfaces import IEventAdapter
from collective.base.interfaces import IAdapter
from collective.base.viewlet import Viewlet
from plone.memoize.view import memoize
from zope.interface import implements


class KeywordsViewlet(Viewlet):
    """Viewlet to show tags"""
    implements(IKeywordsViewlet)
    index = ViewPageTemplateFile('viewlets/keywords.pt')

    def available(self):
        """Return True or False

        :rtype: bool
        """
        if self.categories():
            return True
        else:
            return False

    def categories(self):
        """Return list of dictionary

        :rtype: list
        """
        res = []
        if IATEvent.providedBy(self.context) or IATDocument.providedBy(self.context):
            parent_url = aq_parent(aq_inner(self.context)).absolute_url()
            for category in self.context.Subject():
                res.append({
                    'title': category,
                    'url': '{}?Subject={}'.format(parent_url, category),
                })
        return res


class FolderTagsViewlet(KeywordsViewlet):
    """Viewlet to show tags for conten type: ATFolder"""
    implements(IFolderTagsViewlet)

    def categories(self):
        """Return list of dictionary

        :rtype: list
        """
        res = []
        for category in self.context.Subject():
            res.append({
                'title': category,
                'url': '{}?Subject={}'.format(self.context.absolute_url(), category),
            })
        return res


class BaseRecentViewlet(Viewlet):
    """Base recent box viewlet"""
    implements(IBaseRecentViewlet)
    index = ViewPageTemplateFile('viewlets/recent-box.pt')

    title = None
    parent_folder_id = ''

    def style_class(self):
        """Return class name

        :rtype: unicode
        """
        return self.__name__.split('.')[-1]

    @memoize
    def _path(self):
        """Return path

        :rtype: str
        """
        return '{}/{}'.format(self.context.restrictedTraverse('@@plone').navigationRootPath(), self.parent_folder_id)

    def _subjects(self, brain):
        """Return list of dictionary

        :rtype: list
        """
        res = []
        parent_brain = IAdapter(self.context).get_brain(IATFolder, path=self._path(), depth=0)
        parent_url = parent_brain.getURL()
        for subject in brain.Subject:
            res.append({
                'title': subject,
                'url': '{}?Subject={}'.format(parent_url, subject),
            })
        return res

    @memoize
    def _brain(self):
        """Return brain"""
        return IAdapter(self.context).get_brain(IATDocument, path=self._path(), sort_on='effective', sort_order='descending')

    def item(self):
        """Return dicrionary

        :rtype: dict
        """
        brain = self._brain()
        if brain:
            return {
                'title': brain.Title,
                'description': brain.Description,
                'subjects': self._subjects(brain),
                'url': brain.getURL(),
            }

    def available(self):
        """Return True or False

        :rtype: bool
        """
        if self._brain():
            return True
        else:
            return False


class RecentWorkViewlet(BaseRecentViewlet):
    """Viewlet to show recent work"""
    implements(IRecentWorkViewlet)
    parent_folder_id = 'services'
    title = _(u'Recent work')

    @memoize
    def _brain(self):
        """Return dicrionary

        :rtype: dict
        """
        return IAdapter(self.context).get_brain(IATEvent, path=self._path(), sort_on='end', sort_order='descending')


class RecentBlogViewlet(BaseRecentViewlet):
    """Viewlet to show recent blog"""
    implements(IRecentBlogViewlet)
    parent_folder_id = 'blog'
    title = _(u'Recent blog')


class RecentContributionViewlet(BaseRecentViewlet):
    """Viewlet to show recent contribution"""
    implements(IRecentContributionViewlet)
    parent_folder_id = 'contributions'
    title = _(u'Recent contribution')


class WorkHistoryViewlet(Viewlet):
    """Viewlet: abita.theme.viewlet.work-history for content type: ATFolder"""
    implements(IWorkHistoryViewlet)
    index = ViewPageTemplateFile('viewlets/work-history.pt')

    @memoize
    def works(self):
        """Returns list of dictionary of past works"""
        res = []
        for item in IAdapter(self.context).get_content_listing(IATEvent, depth=1, sort_on='end', sort_order='descending'):
            res.append({
                'client': item.contactName,
                'client_url': item.eventUrl,
                'description': item.Description(),
                'title': item.Title(),
                'url': item.getURL(),
                'year': IEventAdapter(item).year(),
                'end': item.endDate,
            })
        return res

    def year(self):
        """Returns the newest year of works"""
        return self.works()[0]['end'].year()


class WorkHistoryEventViewlet(Viewlet):
    """Viewlet for work history for Event"""
    implements(IWorkHistoryEventViewlet)
    index = ViewPageTemplateFile('viewlets/work-history-event.pt')

    def year(self):
        """Returns year"""
        return IEventAdapter(self.context).year()


class ServicesViewlet(Viewlet):
    """Viewlet: abita.theme.viewlet.services"""
    implements(IServicesViewlet)
    index = ViewPageTemplateFile('viewlets/services.pt')

    def available(self):
        """Return True or False

        :rtype: bool
        """
        if self.services():
            return True
        else:
            return False

    def services(self):
        """Return list of dictionary

        :rtype: list
        """
        res = []
        if 'Subject' not in self.request.form:
            for item in IAdapter(self.context).get_content_listing(IATDocument, depth=1, sort_order='getObjPositionInParent'):
                Subjects = item.Subject()
                if Subjects:
                    Subject = Subjects[0]
                    res.append({
                        'title': item.Title(),
                        'description': item.Description(),
                        'id': item.id,
                        'url': '{}?Subject={}'.format(self.context.absolute_url(), Subject),
                    })
        return res


class ServiceTextViewlet(Viewlet):
    """Viewlet: abita.theme.viewlet.service-text"""
    implements(IServiceTextViewlet)
    index = ViewPageTemplateFile('viewlets/text.pt')

    def available(self):
        """Return True or False

        :rtype: bool
        """
        if self.text():
            return True
        else:
            return False

    @memoize
    def text(self):
        """Return body text

        :rtype: unicode
        """
        if self.view.doc():
            return self.view.doc().CookedBody()


class RecentServiceViewlet(RecentWorkViewlet):
    """Viewlet to show recent service"""
    implements(IRecentServiceViewlet)

    @memoize
    def _brain(self):
        """Return dicrionary

        :rtype: dict
        """
        if self.view.subject():
            return IAdapter(self.context).get_brain(IATEvent, path=self._path(), sort_on='end', sort_order='descending',
                Subject=self.view.subject())
        else:
            return super(RecentServiceViewlet, self)._brain()


class NewsListingViewlet(Viewlet):
    implements(INewsListingViewlet)
    index = ViewPageTemplateFile('viewlets/news-listing.pt')

    def available(self):
        """Return True or False

        :rtype: bool
        """
        if self.news():
            return True
        else:
            return False

    def news(self):
        """Return list of dictionary

        :rtype: list
        """
        query = {'depth': 1, 'sort_order': 'effective', 'review_state': 'published'}
        if self.view.subject():
            query['Subject'] = self.view.subject()
        res = []
        toLocalizedTime = self.context.restrictedTraverse('@@plone').toLocalizedTime
        for item in IAdapter(self.context).get_content_listing(IATNewsItem, **query):
            res.append({
                'title': item.Title(),
                'description': item.Description(),
                'id': item.id,
                'url': item.getURL(),
                'date': toLocalizedTime(item.EffectiveDate()),
                'datetime': item.effective.asdatetime().date().isoformat(),
                'subjects': self._subjects(item),
            })
        return res

    def _subjects(self, item):
        parent_url = aq_parent(aq_inner(self.context)).absolute_url()
        res = []
        for subject in item.Subject():
            res.append({
                'title': subject,
                'url': '{}?Subject={}'.format(parent_url, subject),
            })
        return res
