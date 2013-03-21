from abita.theme.interfaces import IEventAdapter
from five import grok
from plone.memoize.instance import memoize
from zope.interface import Interface


class EventAdapter(grok.Adapter):
    """Adapter for Event"""

    grok.context(Interface)
    grok.provides(IEventAdapter)

    @memoize
    def year(self):
        """Returns year by evaluating start and end date"""
        start_year = self.context.startDate.year()
        end_year = self.context.endDate.year()
        if start_year == end_year:
            return end_year
        else:
            return '{} - {}'.format(start_year, end_year)
