# Copyright (C) 2011 Vaadin Ltd
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)


class VProgressIndicator(Widget, Paintable):
    _CLASSNAME = 'v-progressindicator'
    _wrapper = DOM.createDiv()
    _indicator = DOM.createDiv()
    _client = None
    _poller = None
    _indeterminate = False
    _pollerSuspendedDueDetach = None
    _interval = None

    def __init__(self):
        self.setElement(self.DOM.createDiv())
        self.getElement().appendChild(self._wrapper)
        self.setStyleName(self._CLASSNAME)
        self._wrapper.appendChild(self._indicator)
        self._indicator.setClassName(self._CLASSNAME + '-indicator')
        self._wrapper.setClassName(self._CLASSNAME + '-wrapper')
        self._poller = self.Poller()

    def updateFromUIDL(self, uidl, client):
        self._client = client
        if not uidl.getBooleanAttribute('cached'):
            self._poller.cancel()
        if client.updateComponent(self, uidl, True):
            return
        self._indeterminate = uidl.getBooleanAttribute('indeterminate')
        if self._indeterminate:
            basename = self._CLASSNAME + '-indeterminate'
            VProgressIndicator.setStyleName(self.getElement(), basename, True)
            VProgressIndicator.setStyleName(self.getElement(), basename + '-disabled', uidl.getBooleanAttribute('disabled'))
        else:
            try:
                f = self.float(uidl.getStringAttribute('state'))
                size = self.Math.round(100 * f)
                self.DOM.setStyleAttribute(self._indicator, 'width', size + '%')
            except Exception, e:
                pass # astStmt: [Stmt([]), None]
        if not uidl.getBooleanAttribute('disabled'):
            self._interval = uidl.getIntAttribute('pollinginterval')
            self._poller.scheduleRepeating(self._interval)

    def onAttach(self):
        super(VProgressIndicator, self).onAttach()
        if self._pollerSuspendedDueDetach:
            self._poller.scheduleRepeating(self._interval)

    def onDetach(self):
        super(VProgressIndicator, self).onDetach()
        if self._interval > 0:
            self._poller.cancel()
            self._pollerSuspendedDueDetach = True

    def setVisible(self, visible):
        super(VProgressIndicator, self).setVisible(visible)
        if not visible:
            self._poller.cancel()

    class Poller(Timer):

        def run(self):
            if (
                not self.client.hasActiveRequest() and Util.isAttachedAndDisplayed(_VProgressIndicator_this)
            ):
                self.client.sendPendingVariableChanges()