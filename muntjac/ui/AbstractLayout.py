# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.ui.ILayout import ILayout, IMarginHandler, MarginInfo
from muntjac.ui.AbstractComponentContainer import AbstractComponentContainer
from muntjac.terminal.gwt.client.MouseEventDetails import MouseEventDetails
from muntjac.terminal.gwt.client.EventId import EventId
from muntjac.event.LayoutEvents import ILayoutClickNotifier


class AbstractLayout(AbstractComponentContainer, ILayout, IMarginHandler):
    """An abstract class that defines default implementation for the {@link ILayout}
    interface.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 5.0
    """
    _CLICK_EVENT = EventId.LAYOUT_CLICK

    def __init__(self):
        self.margins = MarginInfo(False)


    def setMargin(self, *args):
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], MarginInfo):
                marginInfo, = args
                self.margins.setMargins(marginInfo)
                self.requestRepaint()
            else:
                enabled, = args
                self.margins.setMargins(enabled)
                self.requestRepaint()
        elif nargs == 4:
            topEnabled, rightEnabled, bottomEnabled, leftEnabled = args
            self.margins.setMargins(topEnabled,
                                    rightEnabled,
                                    bottomEnabled,
                                    leftEnabled)
            self.requestRepaint()
        else:
            raise ValueError, 'invalid number of arguments'


    def getMargin(self):
        return self.margins


    def paintContent(self, target):
        # Add margin info. Defaults to false.
        target.addAttribute('margins', self.margins.getBitMask())


    def changeVariables(self, source, variables):
        super(AbstractLayout, self).changeVariables(source, variables)
        # not all subclasses use these events
        if isinstance(self, ILayoutClickNotifier) \
                and self._CLICK_EVENT in variables:
            self.fireClick(variables[self._CLICK_EVENT])


    def fireClick(self, parameters):
        """Fire a layout click event.

        Note that this method is only used by the subclasses that implement
        {@link LayoutClickNotifier}, and can be overridden for custom click event
        firing.

        @param parameters
                   The parameters received from the client side implementation
        """
        mouseDetails = MouseEventDetails.deSerialize(parameters['mouseDetails'])
        clickedComponent = parameters.get('component')
        childComponent = clickedComponent
        while childComponent is not None and childComponent.getParent() != self:
            childComponent = childComponent.getParent()
        self.fireEvent(self.LayoutClickEvent(self, mouseDetails,
                                             clickedComponent,
                                             childComponent))
