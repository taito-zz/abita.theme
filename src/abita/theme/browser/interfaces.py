from collective.base.interfaces import IBaseView as IBaseBaseView
from collective.base.interfaces import IViewlet
from zope.interface import Attribute
from zope.interface import Interface


# Browser layer

class IAbitaThemeLayer(Interface):
    """Marker interface for browserlayer."""


# View

class IBaseView(IBaseBaseView):
    """Base view interface"""


class IWorkHistoryView(IBaseView):
    """View interface for @@work-history for ATFolder"""


class IWorkHistoryEventView(IBaseView):
    """View interface for @@work-history for ATEvent"""


# Viewlet

class IBaseRecentViewlet(IViewlet):
    """Viewlet interface for recent box"""

    title = Attribute('Title of viewlet')
    parent_folder_id = Attribute('ID for parent folder')

    def style_class():
        """Return class name

        :rtype: unicode
        """

    def item():
        """Return dicrionary

        :rtype: dict
        """


class IRecentBlogViewlet(IBaseRecentViewlet):
    """Viewlet interface to show recent blog"""


class IRecentWorkViewlet(IBaseRecentViewlet):
    """Viewlet interface to show recent work"""


class IWorkHistoryViewlet(IViewlet):
    """Viewlet interface"""


class IWorkHistoryEventViewlet(IViewlet):
    """Viewlet interface for content type: ATEvent"""

    def year():
        """Return year

        :rtype: str
        """
