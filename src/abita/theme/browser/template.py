from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from abita.theme.browser.interfaces import IAbitaThemeLayer
from collective.base.interfaces import IAdapter
from datetime import datetime
from five import grok

grok.templatedir('templates')


class BaseView(grok.View):
    """Base view"""
    grok.baseclass()
    grok.layer(IAbitaThemeLayer)
    grok.require('zope2.View')


class BaseFolderView(BaseView):
    """Base view for Folder"""
    grok.baseclass()
    grok.context(IATFolder)


class WorkHistoryView(BaseFolderView):
    """View for work history"""
    grok.name('work-history')
    grok.template('work-history')

    def works(self):
        """Returns list of dictionary of past works"""
        res = []
        for item in IAdapter(self.context).get_content_listing(IATEvent, depth=1):
            res.append({
                'client': item.contactName,
                'client_url': item.eventUrl,
                'description': item.Description(),
                'url': item.getURL(),
                'year': self._year(item),
            })
        return res

    def year(self):
        """Returns current YEAR"""
        return datetime.now().year

    def _year(self, item):
        """Returns year by evaluating start and end date"""
        start_year = item.startDate.year()
        end_year = item.endDate.year()
        if start_year == end_year:
            return end_year
        else:
            return '{} - {}'.format(start_year, end_year)


class WorkHistoryEventView(BaseView):
    """View for work history for Event"""
    grok.context(IATEvent)
    grok.name('work-history')
    grok.template('work-history-event')
