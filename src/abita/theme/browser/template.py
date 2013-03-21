from Products.ATContentTypes.interfaces.event import IATEvent
from Products.ATContentTypes.interfaces.folder import IATFolder
from abita.theme.browser.interfaces import IAbitaThemeLayer
from abita.theme.interfaces import IEventAdapter
from collective.base.interfaces import IAdapter
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
                'title': item.Title(),
                'url': item.getURL(),
                'year': IEventAdapter(item).year(),
            })
        return res

    def year(self):
        """Returns the newest year of works"""
        return min([item['year'] for item in self.works()])


class WorkHistoryEventView(BaseView):
    """View for work history for Event"""
    grok.context(IATEvent)
    grok.name('work-history')
    grok.template('work-history-event')

    def year(self):
        """Returns year"""
        return IEventAdapter(self.context).year()
