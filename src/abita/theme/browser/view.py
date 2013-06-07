from Products.ATContentTypes.interfaces.document import IATDocument
from abita.theme.browser.interfaces import IBaseSubjectView
from abita.theme.browser.interfaces import IBaseView
from abita.theme.browser.interfaces import INewsListingView
from abita.theme.browser.interfaces import IServicesView
from abita.theme.browser.interfaces import IWorkHistoryEventView
from abita.theme.browser.interfaces import IWorkHistoryView
from collective.base.interfaces import IAdapter
from collective.base.view import BaseView as BaseBaseView
from zope.interface import implements
from plone.memoize.view import memoize


class BaseView(BaseBaseView):
    """Base view"""
    implements(IBaseView)

    def __call__(self):
        return self.template()

    def title(self):
        return self.context.Title()

    def description(self):
        return self.context.Description()


class WorkHistoryView(BaseView):
    """View: @@work-history for content type: ATFolder"""
    implements(IWorkHistoryView)


class WorkHistoryEventView(BaseView):
    """View for work history for Event"""
    implements(IWorkHistoryEventView)


class BaseSubjectView(BaseView):
    """Base view for content type: ATFolder"""
    implements(IBaseSubjectView)

    @memoize
    def subject(self):
        """Return Subject from request or None"""
        return self.request.form.get('Subject')

    @memoize
    def doc(self):
        """Return instance of ATDocument"""
        if self.subject():
            return IAdapter(self.context).get_object(IATDocument, depth=1, Subject=self.subject())

    def title(self):
        if self.doc():
            return self.doc().Title()
        return self.context.Title()

    def description(self):
        if self.doc():
            return self.doc().Description()
        return self.context.Description()


class ServicesView(BaseSubjectView):
    """View: @@services for content type: ATFolder"""
    implements(IServicesView)


class NewsListingView(BaseSubjectView):
    """View: @@news-listing for content type: ATFolder"""
    implements(INewsListingView)
