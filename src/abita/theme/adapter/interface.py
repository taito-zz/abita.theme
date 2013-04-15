from abita.theme.interfaces import IEventAdapter
from plone.memoize.instance import memoize
from zope.interface import implements


class EventAdapter(object):
    """Adapter for Event"""

    implements(IEventAdapter)

    def __init__(self, context):
        self.context = context

    @memoize
    def year(self):
        """Returns year by evaluating start and end date"""
        start_year = self.context.startDate.year()
        end_year = self.context.endDate.year()
        if start_year == end_year:
            return end_year
        else:
            return '{} - {}'.format(start_year, end_year)
