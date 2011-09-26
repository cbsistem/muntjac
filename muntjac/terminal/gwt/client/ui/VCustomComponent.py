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
from com.vaadin.terminal.gwt.client.RenderSpace import (RenderSpace,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
# from java.util.Set import (Set,)


class VCustomComponent(SimplePanel, Container):
    _CLASSNAME = 'v-customcomponent'
    _height = None
    _client = None
    _rendering = None
    _width = None
    _renderSpace = RenderSpace()

    def __init__(self):
        super(VCustomComponent, self)()
        self.setStyleName(self._CLASSNAME)

    def updateFromUIDL(self, uidl, client):
        self._rendering = True
        if client.updateComponent(self, uidl, True):
            self._rendering = False
            return
        self._client = client
        child = uidl.getChildUIDL(0)
        if child is not None:
            p = client.getPaintable(child)
            if p != self.getWidget():
                if self.getWidget() is not None:
                    client.unregisterPaintable(self.getWidget())
                    self.clear()
                self.setWidget(p)
            p.updateFromUIDL(child, client)
        updateDynamicSize = self.updateDynamicSize()
        if updateDynamicSize:
            _VCustomComponent_this = self

            class _0_(Command):

                def execute(self):
                    # FIXME deferred relative size update needed to fix some
                    # scrollbar issues in sampler. This must be the wrong way
                    # to do it. Might be that some other component is broken.
                    self.client.handleComponentRelativeSize(_VCustomComponent_this)

            _0_ = self._0_()
            self.Scheduler.get().scheduleDeferred(_0_)
        self._renderSpace.setWidth(self.getElement().getOffsetWidth())
        self._renderSpace.setHeight(self.getElement().getOffsetHeight())
        # Needed to update client size if the size of this component has
        # changed and the child uses relative size(s).

        client.runDescendentsLayout(self)
        self._rendering = False

    def updateDynamicSize(self):
        updated = False
        if self.isDynamicWidth():
            childWidth = Util.getRequiredWidth(self.getWidget())
            self.getElement().getStyle().setPropertyPx('width', childWidth)
            updated = True
        if self.isDynamicHeight():
            childHeight = Util.getRequiredHeight(self.getWidget())
            self.getElement().getStyle().setPropertyPx('height', childHeight)
            updated = True
        return updated

    def isDynamicWidth(self):
        return (self._width is None) or (self._width == '')

    def isDynamicHeight(self):
        return (self._height is None) or (self._height == '')

    def hasChildComponent(self, component):
        if self.getWidget() == component:
            return True
        else:
            return False

    def replaceChildComponent(self, oldComponent, newComponent):
        if self.hasChildComponent(oldComponent):
            self.clear()
            self.setWidget(newComponent)
        else:
            raise self.IllegalStateException()

    def updateCaption(self, component, uidl):
        # NOP, custom component dont render composition roots caption
        pass

    def requestLayout(self, child):
        return not self.updateDynamicSize()

    def getAllocatedSpace(self, child):
        return self._renderSpace

    def setHeight(self, height):
        super(VCustomComponent, self).setHeight(height)
        self._renderSpace.setHeight(self.getElement().getOffsetHeight())
        if not (height == self._height):
            self._height = height
            if not self._rendering:
                self._client.handleComponentRelativeSize(self.getWidget())

    def setWidth(self, width):
        super(VCustomComponent, self).setWidth(width)
        self._renderSpace.setWidth(self.getElement().getOffsetWidth())
        if not (width == self._width):
            self._width = width
            if not self._rendering:
                self._client.handleComponentRelativeSize(self.getWidget())