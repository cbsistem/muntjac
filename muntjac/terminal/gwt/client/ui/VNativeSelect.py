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
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.ui.VListSelect import (TooltipListBox,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Iterator import (Iterator,)


class VNativeSelect(VOptionGroupBase, Field):
    CLASSNAME = 'v-select'
    select = None
    _firstValueIsTemporaryNullItem = False

    def __init__(self):
        super(VNativeSelect, self)(TooltipListBox(False), self.CLASSNAME)
        self.select = self.optionsContainer
        self.select.setSelect(self)
        self.select.setVisibleItemCount(1)
        self.select.addChangeHandler(self)
        self.select.setStyleName(self.CLASSNAME + '-select')

    def buildOptions(self, uidl):
        self.select.setClient(self.client)
        self.select.setEnabled(not self.isDisabled() and not self.isReadonly())
        self.select.clear()
        self._firstValueIsTemporaryNullItem = False
        if self.isNullSelectionAllowed() and not self.isNullSelectionItemAvailable():
            # can't unselect last item in singleselect mode
            self.select.addItem('', None)
        selected = False
        _0 = True
        i = uidl.getChildIterator()
        while True:
            if _0 is True:
                _0 = False
            if not i.hasNext():
                break
            optionUidl = i.next()
            self.select.addItem(optionUidl.getStringAttribute('caption'), optionUidl.getStringAttribute('key'))
            if optionUidl.hasAttribute('selected'):
                self.select.setItemSelected(self.select.getItemCount() - 1, True)
                selected = True
        if not selected and not self.isNullSelectionAllowed():
            # null-select not allowed, but value not selected yet; add null and
            # remove when something is selected
            self.select.insertItem('', None, 0)
            self.select.setItemSelected(0, True)
            self._firstValueIsTemporaryNullItem = True
        if BrowserInfo.get().isIE6():
            # lazy size change - IE6 uses naive dropdown that does not have a
            # proper size yet
            Util.notifyParentOfSizeChange(self, True)

    def getSelectedItems(self):
        selectedItemKeys = list()
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < self.select.getItemCount()):
                break
            if self.select.isItemSelected(i):
                selectedItemKeys.add(self.select.getValue(i))
        return list([None] * len(selectedItemKeys))

    def onChange(self, event):
        if self.select.isMultipleSelect():
            self.client.updateVariable(self.id, 'selected', self.getSelectedItems(), self.isImmediate())
        else:
            self.client.updateVariable(self.id, 'selected', ['' + self.getSelectedItem()], self.isImmediate())
        if self._firstValueIsTemporaryNullItem:
            # remove temporary empty item
            self.select.removeItem(0)
            self._firstValueIsTemporaryNullItem = False

    def setHeight(self, height):
        self.select.setHeight(height)
        super(VNativeSelect, self).setHeight(height)

    def setWidth(self, width):
        self.select.setWidth(width)
        super(VNativeSelect, self).setWidth(width)

    def setTabIndex(self, tabIndex):
        self.optionsContainer.setTabIndex(tabIndex)

    def focus(self):
        self.select.setFocus(True)