from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class IAbitaThemeLayer(Interface):
    """Marker interface for browserlayer."""


class ITopViewletManager(IViewletManager):
    """A viewlet manager for Portal Top Page."""
