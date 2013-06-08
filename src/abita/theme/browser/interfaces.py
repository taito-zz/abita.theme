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
    """View interface for @@work-history for content type: ATEvent"""


class IBaseSubjectView(IBaseView):
    """Base view interface for @@services for content type: ATFolder"""

    def subject():
        """Return Subject from request or None"""

    def doc():
        """Return object of ATDocument

        :rtype: object
        """


class IServicesView(IBaseSubjectView):
    """View interface for @@services for content type: ATFolder"""


class INewsListingView(IBaseSubjectView):
    """View interface for @@news-listing for content type: ATFolder"""


# Viewlet

class IKeywordsViewlet(IViewlet):
    """Viewlet interface to show tags"""

    def categories():
        """Return list of dictionary

        :rtype: list
        """


class IFolderTagsViewlet(IKeywordsViewlet):
    """Viewlet interface to show tags for content type: ATFolder"""


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


class IRecentWorkViewlet(IBaseRecentViewlet):
    """Viewlet interface to show recent work"""


class IRecentBlogViewlet(IBaseRecentViewlet):
    """Viewlet interface to show recent blog"""


class IRecentContributionViewlet(IBaseRecentViewlet):
    """Viewlet interface to show recent work"""


class IWorkHistoryViewlet(IViewlet):
    """Viewlet interface"""


class IWorkHistoryEventViewlet(IViewlet):
    """Viewlet interface for content type: ATEvent"""

    def year():
        """Return year

        :rtype: str
        """


class IServicesViewlet(IViewlet):
    """Viewlet interface for content type: ATFolder"""

    def services():
        """Return list of dictionary

        :rtype: list
        """


class IServiceTextViewlet(IViewlet):
    """Viewlet interface to show text"""

    def text():
        """Return body text

        :rtype: unicode
        """


class IRecentServiceViewlet(IRecentWorkViewlet):
    """Viewlet interface to show recent service"""


class INewsListingViewlet(IViewlet):
    """Viewlet interface to show news listing"""

    def title():
        """Return title from folder title

        :rtype: str
        """

    def news():
        """Return list of dictionary

        :rtype: list
        """
