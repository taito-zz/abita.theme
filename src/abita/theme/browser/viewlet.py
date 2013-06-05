from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from abita.theme import _
from abita.theme.browser.interfaces import IBaseRecentViewlet
from abita.theme.browser.interfaces import IRecentBlogViewlet
from abita.theme.browser.interfaces import IRecentWorkViewlet
from abita.theme.browser.interfaces import IWorkHistoryEventViewlet
from abita.theme.browser.interfaces import IWorkHistoryViewlet
from abita.theme.interfaces import IEventAdapter
from collective.base.interfaces import IAdapter
from collective.base.viewlet import Viewlet
from plone.memoize.view import memoize
from zope.interface import implements


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
        for subject in brain.Subject:
            bra = IAdapter(self.context).get_brain(IATFolder, path=self._path(), depth=1, Subject=subject)
            if bra:
                res.append({
                    'title': bra.Title,
                    'description': bra.Description,
                    'url': bra.getURL(),
                })
            else:
                res.append({
                    'title': subject,
                    'description': None,
                    'url': None,
                })
        brain = IAdapter(self.context).get_brain(IATFolder, path=self._path(), depth=0)
        if brain:
            res.append({
                'title': brain.Title,
                'description': brain.Description,
                'url': brain.getURL(),
            })
        return res

    def _brain(self):
        """Return brain"""

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


class RecentBlogViewlet(BaseRecentViewlet):
    """Viewlet to show recent blog"""
    implements(IRecentBlogViewlet)
    parent_folder_id = 'blog'
    title = _(u'Recent blog')

    @memoize
    def _brain(self):
        return IAdapter(self.context).get_brain(IATDocument, path=self._path(), sort_on='effective', sort_order='descending')


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
    """View for work history for Event"""
    implements(IWorkHistoryEventViewlet)
    index = ViewPageTemplateFile('viewlets/work-history-event.pt')

    def year(self):
        """Returns year"""
        return IEventAdapter(self.context).year()
