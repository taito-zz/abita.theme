from abita.utils.utils import reimport_profile

import logging


PROFILE_ID = 'profile-abita.theme:default'


def show_path_bar(context, logger=None):
    """Show path bar"""
    if logger is None:
        logger = logging.getLogger(__name__)
    from zope.component import getUtility
    from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
    storage = getUtility(IViewletSettingsStorage)
    manager = "plone.abovecontent"
    storage.setHidden(manager, "Plone Default", ())
    storage.setHidden(manager, 'Plone Classic Theme', ())
    storage.setHidden(manager, 'Sunburst Theme', ())


def reimport_viewlets(context, logger=None):
    """Reimport viewlets"""
    reimport_profile(context, PROFILE_ID, 'viewlets')


def reimport_typeinfo(context):
    """Update typeinfo"""
    reimport_profile(context, PROFILE_ID, 'typeinfo')
