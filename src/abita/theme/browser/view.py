from abita.theme.browser.interfaces import IBaseView
from abita.theme.browser.interfaces import IWorkHistoryEventView
from abita.theme.browser.interfaces import IWorkHistoryView
from collective.base.view import BaseView as BaseBaseView
from zope.interface import implements


class BaseView(BaseBaseView):
    """Base view"""
    implements(IBaseView)

    def __call__(self):
        super(BaseView, self).__call__()
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
