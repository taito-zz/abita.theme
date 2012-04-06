from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.formlib import form
from zope.interface import implements

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base


class IFirefoxPortlet(IPortletDataProvider):

    pass


class Assignment(base.Assignment):
    implements(IFirefoxPortlet)

    @property
    def title(self):
        return _(u"Recommend Firefox!")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('firefox.pt')

    @property
    def available(self):
        items = ['Gecko', 'AppleWebKit']
        agent = self.request.get('HTTP_USER_AGENT')
        for item in items:
            if item in agent:
                return False
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IFirefoxPortlet)
    label = _(u"Add Firefox Portlet")
    description = _(u"This portlet recommends firefox.")

    def create(self):
        return Assignment()
