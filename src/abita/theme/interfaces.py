from zope.interface import Interface


class IEventAdapter(Interface):
    """Interface for Event adapter"""

    def year():  # pragma: no cover
        """Returns year by evaluating start and end date"""
