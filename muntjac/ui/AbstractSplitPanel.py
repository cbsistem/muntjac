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

from muntjac.event.IComponentEventListener import IComponentEventListener
from muntjac.ui.VerticalLayout import VerticalLayout
from muntjac.ui.AbstractLayout import AbstractLayout
from muntjac.terminal.gwt.client.MouseEventDetails import MouseEventDetails
from muntjac.event.MouseEvents import ClickEvent as MouseClickEvent

from muntjac.terminal.gwt.client.ui.VSplitPanel import VSplitPanel


class ComponentIterator(object):  # FIXME: implement iterator
    """Modifiable and Serializable Iterator for the components, used by
    {@link AbstractSplitPanel#getComponentIterator()}.
    """

    def __init__(self, sp):
        self.sp = sp
        self._i = 0


    def hasNext(self):
        if self._i < self.sp.getComponentCount():
            return True
        return False


    def __iter__(self):
        if not self.hasNext():
            return None
        self._i += 1
        if self._i == 1:
            return self.sp.secondComponent if self.sp.firstComponent is None else self.sp.firstComponent
        elif self._i == 2:
            return self.sp.secondComponent
        return None


    def remove(self):
        if self._i == 1:
            if self.sp.firstComponent is not None:
                self.sp.setFirstComponent(None)
                self._i = 0
            else:
                self.sp.setSecondComponent(None)
        elif self._i == 2:
            self.sp.setSecondComponent(None)


class AbstractSplitPanel(AbstractLayout):
    """AbstractSplitPanel.

    <code>AbstractSplitPanel</code> is base class for a component container that
    can contain two components. The comopnents are split by a divider element.

    @author Vaadin Ltd.
    @version @VERSION@
    @since 6.5
    """

    _SPLITTER_CLICK_EVENT = VSplitPanel.SPLITTER_CLICK_EVENT_IDENTIFIER

    def __init__(self):
        self._firstComponent = None
        self._secondComponent = None
        self._pos = 50
        self._posUnit = self.UNITS_PERCENTAGE
        self._posReversed = False
        self._locked = False


    def addComponent(self, c):
        """Add a component into this container. The component is added to the right
        or under the previous component.

        @param c
                   the component to be added.
        """
        if self._firstComponent is None:
            self._firstComponent = c
        elif self._secondComponent is None:
            self._secondComponent = c
        else:
            raise NotImplementedError, 'Split panel can contain only two components'

        super(AbstractSplitPanel, self).addComponent(c)
        self.requestRepaint()


    def setFirstComponent(self, c):
        if self._firstComponent == c:
            # Nothing to do
            return

        if self._firstComponent is not None:
            # detach old
            self.removeComponent(self._firstComponent)

        self._firstComponent = c
        super(AbstractSplitPanel, self).addComponent(c)
        self.requestRepaint()


    def setSecondComponent(self, c):
        if c == self._secondComponent:
            # Nothing to do
            return

        if self._secondComponent is not None:
            # detach old
            self.removeComponent(self._secondComponent)

        self._secondComponent = c
        super(AbstractSplitPanel, self).addComponent(c)
        self.requestRepaint()


    def getFirstComponent(self):
        """@return the first component of this SplitPanel."""
        return self._firstComponent


    def getSecondComponent(self):
        """@return the second component of this SplitPanel."""
        return self._secondComponent


    def removeComponent(self, c):
        """Removes the component from this container.

        @param c
                   the component to be removed.
        """
        super(AbstractSplitPanel, self).removeComponent(c)

        if c == self._firstComponent:
            self._firstComponent = None
        elif c == self._secondComponent:
            self._secondComponent = None

        self.requestRepaint()


    def getComponentIterator(self):
        return ComponentIterator(self)


    def getComponentCount(self):
        """Gets the number of contained components. Consistent with the iterator
        returned by {@link #getComponentIterator()}.

        @return the number of contained components (zero, one or two)
        """
        count = 0
        if self._firstComponent is not None:
            count += 1

        if self._secondComponent is not None:
            count += 1

        return count



    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the paint operation failed.
        """
        super(AbstractSplitPanel, self).paintContent(target)

        position = self._pos + self.UNIT_SYMBOLS[self._posUnit]

        target.addAttribute('position', position)

        if self.isLocked():
            target.addAttribute('locked', True)

        target.addAttribute('reversed', self._posReversed)

        if self._firstComponent is not None:
            self._firstComponent.paint(target)
        else:
            temporaryComponent = VerticalLayout()
            temporaryComponent.setParent(self)
            temporaryComponent.paint(target)
        if self._secondComponent is not None:
            self._secondComponent.paint(target)
        else:
            temporaryComponent = VerticalLayout()
            temporaryComponent.setParent(self)
            temporaryComponent.paint(target)


    def replaceComponent(self, oldComponent, newComponent):

        if oldComponent == self._firstComponent:
            self.setFirstComponent(newComponent)
        elif oldComponent == self._secondComponent:
            self.setSecondComponent(newComponent)

        self.requestRepaint()


    def setSplitPosition(self, *args):
        """Moves the position of the splitter.

        @param pos
                   the new size of the first region in the unit that was last
                   used (default is percentage)
        ---
        Moves the position of the splitter.

        @param pos
                   the new size of the region in the unit that was last used
                   (default is percentage)
        @param reverse
                   if set to true the split splitter position is measured by the
                   second region else it is measured by the first region
        ---
        Moves the position of the splitter with given position and unit.

        @param pos
                   size of the first region
        @param unit
                   the unit (from {@link Sizeable}) in which the size is given.
        ---
        Moves the position of the splitter with given position and unit.

        @param pos
                   size of the first region
        @param unit
                   the unit (from {@link Sizeable}) in which the size is given.
        @param reverse
                   if set to true the split splitter position is measured by the
                   second region else it is measured by the first region
        ---
        Moves the position of the splitter.

        @param pos
                   the new size of the first region
        @param unit
                   the unit (from {@link Sizeable}) in which the size is given.
        @param repaintNotNeeded
                   true if client side needs to be updated. Use false if the
                   position info has come from the client side, thus it already
                   knows the position.
        """
        nargs = len(args)
        if nargs == 1:
            pos, = args
            self.setSplitPosition(pos, self._posUnit, True, False)
        elif nargs == 2:
            if isinstance(args[1], bool):
                pos, reverse = args
                self.setSplitPosition(pos, self._posUnit, True, reverse)
            else:
                pos, unit = args
                self.setSplitPosition(pos, unit, True, False)
        elif nargs == 3:
            pos, unit, reverse = args
            self.setSplitPosition(pos, unit, True, reverse)
        elif nargs == 4:
            pos, unit, repaintNeeded, reverse = args
            if unit != self.UNITS_PERCENTAGE and unit != self.UNITS_PIXELS:
                raise self.IllegalArgumentException('Only percentage and pixel units are allowed')
            self._pos = pos
            self._posUnit = unit
            self._posReversed = reverse
            if repaintNeeded:
                self.requestRepaint()
        else:
            raise ValueError, 'too many arguments'


    def getSplitPosition(self):
        """Returns the current position of the splitter, in
        {@link #getSplitPositionUnit()} units.

        @return position of the splitter
        """
        return self._pos


    def getSplitPositionUnit(self):
        """Returns the unit of position of the splitter

        @return unit of position of the splitter
        """
        return self._posUnit


    def setLocked(self, locked):
        """Lock the SplitPanels position, disabling the user from dragging the split
        handle.

        @param locked
                   Set <code>true</code> if locked, <code>false</code> otherwise.
        """
        self._locked = locked
        self.requestRepaint()


    def isLocked(self):
        """Is the SplitPanel handle locked (user not allowed to change split
        position by dragging).

        @return <code>true</code> if locked, <code>false</code> otherwise.
        """
        # Invoked when a variable of the component changes. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        return self._locked


    def changeVariables(self, source, variables):
        super(AbstractSplitPanel, self).changeVariables(source, variables)

        if 'position' in variables and not self.isLocked():
            newPos = variables['position']
            self.setSplitPosition(newPos, self._posUnit, self._posReversed)

        if self._SPLITTER_CLICK_EVENT in variables:
            self.fireClick(variables[self._SPLITTER_CLICK_EVENT])


    def fireClick(self, parameters):
        mouseDetails = MouseEventDetails.deSerialize(parameters.get('mouseDetails'))
        self.fireEvent( SplitterClickEvent(self, mouseDetails) )


    def addListener(self, listener):
        self.addListener(self._SPLITTER_CLICK_EVENT, SplitterClickEvent, listener, SplitterClickListener.clickMethod)


    def removeListener(self, listener):
        self.removeListener(self._SPLITTER_CLICK_EVENT, SplitterClickEvent, listener)


class SplitterClickListener(IComponentEventListener):
    """<code>SplitterClickListener</code> interface for listening for
    <code>SplitterClickEvent</code> fired by a <code>SplitPanel</code>.

    @see SplitterClickEvent
    @since 6.2
    """

    def splitterClick(self, event):
        """SplitPanel splitter has been clicked

        @param event
                   SplitterClickEvent event.
        """
        pass

    clickMethod = splitterClick  # FIXME: translate findMethod


class SplitterClickEvent(MouseClickEvent):

    def __init__(self, source, mouseEventDetails):
        super(SplitterClickEvent, self)(source, mouseEventDetails)
