from Products.ATContentTypes.interfaces.event import IATEvent
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from abita.theme.interfaces import IEventAdapter
from collective.base.interfaces import IAdapter


class WorkHistoryView(BrowserView):
    """View for work history"""

    __call__ = ViewPageTemplateFile('templates/work-history.pt')

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


class WorkHistoryEventView(BrowserView):
    """View for work history for Event"""

    __call__ = ViewPageTemplateFile('templates/work-history-event.pt')

    def year(self):
        """Returns year"""
        return IEventAdapter(self.context).year()
