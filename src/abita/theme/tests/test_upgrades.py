import mock
import unittest


class UpgradesTestCase(unittest.TestCase):
    """TestCase for upgrade step"""

    def test_reimport_viewlets(self):
        from abita.theme.upgrades import reimport_viewlets
        step = mock.Mock()
        reimport_viewlets(step)
        step.runImportStepFromProfile.assert_called_with('profile-abita.theme:default', 'viewlets',
            run_dependencies=False, purge_old=False)

    def test_reimport_typeinfo(self):
        from abita.theme.upgrades import reimport_typeinfo
        step = mock.Mock()
        reimport_typeinfo(step)
        step.runImportStepFromProfile.assert_called_with('profile-abita.theme:default', 'typeinfo',
            run_dependencies=False, purge_old=False)
