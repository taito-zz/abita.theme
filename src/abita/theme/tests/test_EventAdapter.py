from abita.theme.interfaces import IEventAdapter
from abita.theme.tests.base import IntegrationTestCase

import mock


class EventAdapterTestCase(IntegrationTestCase):
    """TestCase for EventAdapter"""

    def test_year(self):
        item = mock.Mock()
        item.startDate.year.return_value = '2010'
        item.endDate.year.return_value = '2012'
        self.assertEqual(IEventAdapter(item).year(), '2010 - 2012')
