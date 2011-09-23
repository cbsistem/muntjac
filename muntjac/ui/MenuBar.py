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

from Queue import LifoQueue

from muntjac.ui.AbstractComponent import AbstractComponent
from muntjac.terminal.gwt.client.ui.VMenuBar import VMenuBar
from muntjac.ui.ClientWidget import LoadStyle
from muntjac.terminal.gwt.client.ui.MenuItem import MenuItem


class MenuBar(AbstractComponent):
    """<p>
    A class representing a horizontal menu bar. The menu can contain MenuItem
    objects, which in turn can contain more MenuBars. These sub-level MenuBars
    are represented as vertical menu.
    </p>
    """

    CLIENT_WIDGET = VMenuBar
    LOAD_STYLE = LoadStyle.LAZY

    def __init__(self):
        """Constructs an empty, horizontal menu"""
        # Items of the top-level menu
        self._menuItems = list()

        # Number of items in this menu
        self._numberOfItems = 0

        self._collapseItems = None
        self._submenuIcon = None
        self._moreItem = None
        self._openRootOnHover = None

        self.setCollapse(True)
        self.setMoreMenuItem(None)


    def paintContent(self, target):
        """Paint (serialise) the component for the client."""

        # Superclass writes any common attributes in the paint target.
        super(MenuBar, self).paintContent(target)

        target.addAttribute(VMenuBar.OPEN_ROOT_MENU_ON_HOWER, self._openRootOnHover)

        target.startTag('options')

        if self._submenuIcon is not None:
            target.addAttribute('submenuIcon', self._submenuIcon)

        if self.getWidth() > -1:
            target.startTag('moreItem')
            target.addAttribute('text', self._moreItem.getText())
            if self._moreItem.getIcon() is not None:
                target.addAttribute('icon', self._moreItem.getIcon())
            target.endTag('moreItem')

        target.endTag('options')
        target.startTag('items')

        # This generates the tree from the contents of the menu
        for item in self._menuItems:
            self.paintItem(target, item)

        target.endTag('items')


    def paintItem(self, target, item):
        if not item.isVisible():
            return

        target.startTag('item')

        target.addAttribute('id', item.getId())

        if item.getStyleName() is not None:
            target.addAttribute('style', item.getStyleName())

        if item.isSeparator():
            target.addAttribute('separator', True)
        else:
            target.addAttribute('text', item.getText())

            command = item.getCommand()
            if command is not None:
                target.addAttribute('command', True)

            icon = item.getIcon()
            if icon is not None:
                target.addAttribute('icon', icon)

            if not item.isEnabled():
                target.addAttribute('disabled', True)

            description = item.getDescription()
            if description is not None and len(description) > 0:
                target.addAttribute('description', description)

            if item.isCheckable():
                # if the "checked" attribute is present (either true or false),
                # the item is checkable
                target.addAttribute(VMenuBar.ATTRIBUTE_CHECKED, item.isChecked())

            if item.hasChildren():
                for child in item.getChildren():
                    self.paintItem(target, child)

        target.endTag('item')


    def changeVariables(self, source, variables):
        """Deserialize changes received from client."""
        items = LifoQueue()
        found = False

        if 'clickedId' in variables:
            clickedId = variables.get('clickedId')
            for itm in self.getItems():
                items.put(itm)

            tmpItem = None

            # Go through all the items in the menu
            while not found and not items.empty():
                tmpItem = items.pop()
                found = clickedId.intValue() == tmpItem.getId()

                if tmpItem.hasChildren():
                    itr = iter(tmpItem.getChildren())  # FIXME translate iterator
                    while itr.hasNext():
                        items.put(itr.next())

            # If we got the clicked item, launch the command.
            if found and tmpItem.isEnabled():
                if tmpItem.isCheckable():
                    tmpItem.setChecked(not tmpItem.isChecked())

                if None is not tmpItem.getCommand():
                    tmpItem.getCommand().menuSelected(tmpItem)


    def addItem(self, *args):
        """Add a new item to the menu bar. Command can be null, but a caption must
        be given.

        @param caption
                   the text for the menu item
        @param command
                   the command for the menu item
        @throws IllegalArgumentException
        ---
        Add a new item to the menu bar. Icon and command can be null, but a
        caption must be given.

        @param caption
                   the text for the menu item
        @param icon
                   the icon for the menu item
        @param command
                   the command for the menu item
        @throws IllegalArgumentException
        """
        nargs = len(args)
        if nargs == 2:
            caption, command = args
            return self.addItem(caption, None, command)
        elif nargs == 3:
            caption, icon, command = args
            if caption is None:
                raise ValueError, 'caption cannot be null'
            newItem = MenuItem(caption, icon, command, self)
            self._menuItems.add(newItem)
            self.requestRepaint()
            return newItem
        else:
            raise ValueError, 'invalid number of arguments'


    def addItemBefore(self, caption, icon, command, itemToAddBefore):
        """Add an item before some item. If the given item does not exist the item
        is added at the end of the menu. Icon and command can be null, but a
        caption must be given.

        @param caption
                   the text for the menu item
        @param icon
                   the icon for the menu item
        @param command
                   the command for the menu item
        @param itemToAddBefore
                   the item that will be after the new item
        @throws IllegalArgumentException
        """
        if caption is None:
            raise ValueError, 'caption cannot be null'

        newItem = MenuItem(caption, icon, command, self)
        if itemToAddBefore in self._menuItems:
            index = self._menuItems.index(itemToAddBefore)
            self._menuItems.insert(index, newItem)
        else:
            self._menuItems.append(newItem)

        self.requestRepaint()

        return newItem


    def getItems(self):
        """Returns a list with all the MenuItem objects in the menu bar

        @return a list containing the MenuItem objects in the menu bar
        """
        return self._menuItems


    def removeItem(self, item):
        """Remove first occurrence the specified item from the main menu

        @param item
                   The item to be removed
        """
        if item is not None:
            self._menuItems.remove(item)
        self.requestRepaint()


    def removeItems(self):
        """Empty the menu bar"""
        self._menuItems.clear()
        self.requestRepaint()


    def getSize(self):
        """Returns the size of the menu.

        @return The size of the menu
        """
        return len(self._menuItems)


    def setSubmenuIcon(self, icon):
        """Set the icon to be used if a sub-menu has children. Defaults to null;

        @param icon
        @deprecated (since 6.2, will be removed in 7.0) Icon is set in theme, no
                    need to worry about the visual representation here.
        """
        self._submenuIcon = icon
        self.requestRepaint()


    def getSubmenuIcon(self):
        """@deprecated
        @see #setSubmenuIcon(Resource)
        """
        return self._submenuIcon


    def setCollapse(self, collapse):
        """Enable or disable collapsing top-level items. Top-level items will
        collapse together if there is not enough room for them. Items that don't
        fit will be placed under the "More" menu item.

        Collapsing is enabled by default.

        @param collapse
        @deprecated (since 6.2, will be removed in 7.0) Collapsing is always
                    enabled if the MenuBar has a specified width.
        """
        self._collapseItems = collapse
        self.requestRepaint()


    def getCollapse(self):
        """@see #setCollapse(boolean)
        @deprecated
        """
        return self._collapseItems


    def setMoreMenuItem(self, item):
        """Set the item that is used when collapsing the top level menu. All
        "overflowing" items will be added below this. The item command will be
        ignored. If set to null, the default item with a downwards arrow is used.

        The item command (if specified) is ignored.

        @param item
        """
        if item is not None:
            self._moreItem = item
        else:
            self._moreItem = MenuItem('', None, None)
        self.requestRepaint()


    def getMoreMenuItem(self):
        """Get the MenuItem used as the collapse menu item.

        @return
        """
        return self._moreItem


    def setAutoOpen(self, autoOpenTopLevelMenu):
        """Using this method menubar can be put into a special mode where top level
        menus opens without clicking on the menu, but automatically when mouse
        cursor is moved over the menu. In this mode the menu also closes itself
        if the mouse is moved out of the opened menu.
        <p>
        Note, that on touch devices the menu still opens on a click event.

        @param autoOpenTopLevelMenu
                   true if menus should be opened without click, the default is
                   false
        """
        if autoOpenTopLevelMenu != self._openRootOnHover:
            self._openRootOnHover = autoOpenTopLevelMenu
            self.requestRepaint()


    def isAutoOpen(self):
        """Detects whether the menubar is in a mode where top level menus are
        automatically opened when the mouse cursor is moved over the menu.
        Normally root menu opens only by clicking on the menu. Submenus always
        open automatically.

        @return true if the root menus open without click, the default is false
        """
        return self._openRootOnHover


class Command(object):
    """This interface contains the layer for menu commands of the
    {@link com.vaadin.ui.MenuBar} class. It's method will fire when the user
    clicks on the containing {@link com.vaadin.ui.MenuBar.MenuItem}. The
    selected item is given as an argument.
    """

    def menuSelected(self, selectedItem):
        pass


class MenuItem(object):
    """A composite class for menu items and sub-menus. You can set commands to
    be fired on user click by implementing the
    {@link com.vaadin.ui.MenuBar.Command} interface. You can also add
    multiple MenuItems to a MenuItem and create a sub-menu.
    """

    def __init__(self, caption, icon, command, menu):  ## FIXME implement nested class
        """Constructs a new menu item that can optionally have an icon and a
        command associated with it. Icon and command can be null, but a
        caption must be given.

        @param text
                   The text associated with the command
        @param command
                   The command to be fired
        @throws IllegalArgumentException
        """
        self._menu = menu

        self._itsId = None
        self._itsCommand = None
        self._itsText = None
        self._itsChildren = None
        self._itsIcon = None
        self._itsParent = None
        self._enabled = True
        self._visible = True
        self._isSeparator = False
        self._styleName = None
        self._description = None
        self._checkable = False
        self._checked = False

        if caption is None:
            raise ValueError, 'caption cannot be null'

        menu._numberOfItems = menu._numberOfItems + 1
        self._itsId = menu._numberOfItems
        self._itsText = caption
        self._itsIcon = icon
        self._itsCommand = command


    def hasChildren(self):
        """Checks if the item has children (if it is a sub-menu).

        @return True if this item has children
        """
        return not self._isSeparator() and self._itsChildren is not None


    def addSeparator(self):
        """Adds a separator to this menu. A separator is a way to visually group
        items in a menu, to make it easier for users to find what they are
        looking for in the menu.

        @author Jouni Koivuviita / IT Mill Ltd.
        @since 6.2.0
        """
        item = self.addItem('', None, None)
        item.setSeparator(True)
        return item


    def addSeparatorBefore(self, itemToAddBefore):
        item = self.addItemBefore('', None, None, itemToAddBefore)
        item.setSeparator(True)
        return item


    def addItem(self, *args):
        """Add a new item inside this item, thus creating a sub-menu. Command
        can be null, but a caption must be given.

        @param caption
                   the text for the menu item
        @param command
                   the command for the menu item
        ---
        Add a new item inside this item, thus creating a sub-menu. Icon and
        command can be null, but a caption must be given.

        @param caption
                   the text for the menu item
        @param icon
                   the icon for the menu item
        @param command
                   the command for the menu item
        @throws IllegalStateException
                    If the item is checkable and thus cannot have children.
        """
        nargs = len(args)
        if nargs == 2:
            caption, command = args
            return self.addItem(caption, None, command)
        elif nargs == 3:
            caption, icon, command = args
            if self._isSeparator():
                raise NotImplementedError, 'Cannot add items to a separator'
            if self.isCheckable():
                raise ValueError, 'A checkable item cannot have children'
            if caption is None:
                raise ValueError, 'Caption cannot be null'
            if self._itsChildren is None:
                self._itsChildren = list()
            newItem = MenuItem(caption, icon, command, self._menu)  # FIXME implement nested class
            # The only place where the parent is set
            newItem.setParent(self)
            self._itsChildren.add(newItem)
            self.requestRepaint()
            return newItem
        else:
            raise ValueError, 'invalid number of arguments'


    def addItemBefore(self, caption, icon, command, itemToAddBefore):
        """Add an item before some item. If the given item does not exist the
        item is added at the end of the menu. Icon and command can be null,
        but a caption must be given.

        @param caption
                   the text for the menu item
        @param icon
                   the icon for the menu item
        @param command
                   the command for the menu item
        @param itemToAddBefore
                   the item that will be after the new item
        @throws IllegalStateException
                    If the item is checkable and thus cannot have children.
        """
        if self.isCheckable():
            raise ValueError, 'A checkable item cannot have children'

        newItem = None

        if self.hasChildren() and itemToAddBefore in self._itsChildren:
            index = self._itsChildren.index(itemToAddBefore)
            newItem = MenuItem(caption, icon, command, self._menu)  # FIXME implement nested class
            newItem.setParent(self)
            self._itsChildren.add(index, newItem)
        else:
            newItem = self.addItem(caption, icon, command)
        self.requestRepaint()
        return newItem


    def getCommand(self):
        """For the associated command.

        @return The associated command, or null if there is none
        """
        return self._itsCommand


    def getIcon(self):
        """Gets the objects icon.

        @return The icon of the item, null if the item doesn't have an icon
        """
        return self._itsIcon


    def getParent(self):
        """For the containing item. This will return null if the item is in the
        top-level menu bar.

        @return The containing {@link com.vaadin.ui.MenuBar.MenuItem} , or
                null if there is none
        """
        return self._itsParent


    def getChildren(self):
        """This will return the children of this item or null if there are none.

        @return List of children items, or null if there are none
        """
        return self._itsChildren


    def getText(self):
        """Gets the objects text

        @return The text
        """
        return self._itsText


    def getSize(self):
        """Returns the number of children.

        @return The number of child items
        """
        if self._itsChildren is not None:
            return len(self._itsChildren)
        return -1


    def getId(self):
        """Get the unique identifier for this item.

        @return The id of this item
        """
        return self._itsId


    def setCommand(self, command):
        """Set the command for this item. Set null to remove.

        @param command
                   The MenuCommand of this item
        """
        self._itsCommand = command


    def setIcon(self, icon):
        """Sets the icon. Set null to remove.

        @param icon
                   The icon for this item
        """
        self._itsIcon = icon
        self.requestRepaint()


    def setText(self, text):
        """Set the text of this object.

        @param text
                   Text for this object
        """
        if text is not None:
            self._itsText = text
        self.requestRepaint()


    def removeChild(self, item):
        """Remove the first occurrence of the item.

        @param item
                   The item to be removed
        """
        if item is not None and self._itsChildren is not None:
            self._itsChildren.remove(item)
            if self._itsChildren.isEmpty():
                self._itsChildren = None
            self.requestRepaint()


    def removeChildren(self):
        """Empty the list of children items."""
        if self._itsChildren is not None:
            self._itsChildren.clear()
            self._itsChildren = None
            self.requestRepaint()


    def setParent(self, parent):
        """Set the parent of this item. This is called by the addItem method.

        @param parent
                   The parent item
        """
        self._itsParent = parent


    def setEnabled(self, enabled):
        self._enabled = enabled
        self.requestRepaint()


    def isEnabled(self):
        return self._enabled


    def setVisible(self, visible):
        self._visible = visible
        self.requestRepaint()


    def isVisible(self):
        return self._visible


    def setSeparator(self, isSeparator):
        self._isSeparator = isSeparator
        self.requestRepaint()


    def isSeparator(self):
        return self._isSeparator


    def setStyleName(self, styleName):
        self._styleName = styleName
        self.requestRepaint()


    def getStyleName(self):
        return self._styleName


    def setDescription(self, description):
        """Sets the items's description. See {@link #getDescription()} for more
        information on what the description is. This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.

        @param description
                   the new description string for the component.
        """
        self._description = description
        self.requestRepaint()


    def getDescription(self):
        """<p>
        Gets the items's description. The description can be used to briefly
        describe the state of the item to the user. The description string
        may contain certain XML tags:
        </p>

        <p>
        <table border=1>
        <tr>
        <td width=120><b>Tag</b></td>
        <td width=120><b>Description</b></td>
        <td width=120><b>Example</b></td>
        </tr>
        <tr>
        <td>&lt;b></td>
        <td>bold</td>
        <td><b>bold text</b></td>
        </tr>
        <tr>
        <td>&lt;i></td>
        <td>italic</td>
        <td><i>italic text</i></td>
        </tr>
        <tr>
        <td>&lt;u></td>
        <td>underlined</td>
        <td><u>underlined text</u></td>
        </tr>
        <tr>
        <td>&lt;br></td>
        <td>linebreak</td>
        <td>N/A</td>
        </tr>
        <tr>
        <td>&lt;ul><br>
        &lt;li>item1<br>
        &lt;li>item1<br>
        &lt;/ul></td>
        <td>item list</td>
        <td>
        <ul>
        <li>item1
        <li>item2
        </ul>
        </td>
        </tr>
        </table>
        </p>

        <p>
        These tags may be nested.
        </p>

        @return item's description <code>String</code>
        """
        return self._description


    def isCheckable(self):
        """Gets the checkable state of the item - whether the item has checked
        and unchecked states. If an item is checkable its checked state (as
        returned by {@link #isChecked()}) is indicated in the UI.

        <p>
        An item is not checkable by default.
        </p>

        @return true if the item is checkable, false otherwise
        @since 6.6.2
        """
        return self._checkable


    def setCheckable(self, checkable):
        """Sets the checkable state of the item. If an item is checkable its
        checked state (as returned by {@link #isChecked()}) is indicated in
        the UI.

        <p>
        An item is not checkable by default.
        </p>

        <p>
        Items with sub items cannot be checkable.
        </p>

        @param checkable
                   true if the item should be checkable, false otherwise
        @throws IllegalStateException
                    If the item has children
        @since 6.6.2
        """
        if self.hasChildren():
            raise ValueError, 'A menu item with children cannot be checkable'
        self._checkable = checkable
        self.requestRepaint()


    def isChecked(self):
        """Gets the checked state of the item (checked or unchecked). Only used
        if the item is checkable (as indicated by {@link #isCheckable()}).
        The checked state is indicated in the UI with the item, if the item
        is checkable.

        <p>
        An item is not checked by default.
        </p>

        <p>
        The CSS style corresponding to the checked state is "-checked".
        </p>

        @return true if the item is checked, false otherwise
        @since 6.6.2
        """
        return self._checked


    def setChecked(self, checked):
        """Sets the checked state of the item. Only used if the item is
        checkable (indicated by {@link #isCheckable()}). The checked state is
        indicated in the UI with the item, if the item is checkable.

        <p>
        An item is not checked by default.
        </p>

        <p>
        The CSS style corresponding to the checked state is "-checked".
        </p>

        @return true if the item is checked, false otherwise
        @since 6.6.2
        """
        self._checked = checked
        self.requestRepaint()
