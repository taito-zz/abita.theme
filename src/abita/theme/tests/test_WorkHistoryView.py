from abita.theme.browser.template import WorkHistoryView
from abita.theme.tests.base import IntegrationTestCase

import mock


class WorkHistoryViewTestCase(IntegrationTestCase):
    """TestCase for WorkHistoryView"""

    def test__year(self):
        folder = self.create_atcontent('Folder', id='folder')
        instance = self.create_view(WorkHistoryView, context=folder)
        item = mock.Mock()
        item.startDate.year.return_value = '2010'
        item.endDate.year.return_value = '2012'
        self.assertEqual(instance._year(item), '2010 - 2012')
