from zope.interface import Interface


class IEventAdapter(Interface):
    """Interface for Event adapter"""

    def year():
        """Returns year by evaluating start and end date"""
