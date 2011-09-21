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


class Terminal(object):
    """An interface that provides information about the user's terminal.
    Implementors typically provide additional information using methods not in
    this interface. </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def getDefaultTheme(self):
        """Gets the name of the default theme for this terminal.

        @return the name of the theme that is used by default by this terminal.
        """
        pass


    def getScreenWidth(self):
        """Gets the width of the terminal screen in pixels. This is the width of the
        screen and not the width available for the application.
        <p>
        Note that the screen width is typically not available in the
        {@link com.vaadin.Application#init()} method as this is called before the
        browser has a chance to report the screen size to the server.
        </p>

        @return the width of the terminal screen.
        """
        pass


    def getScreenHeight(self):
        """Gets the height of the terminal screen in pixels. This is the height of
        the screen and not the height available for the application.

        <p>
        Note that the screen height is typically not available in the
        {@link com.vaadin.Application#init()} method as this is called before the
        browser has a chance to report the screen size to the server.
        </p>

        @return the height of the terminal screen.
        """
        pass


class ErrorEvent(object):
    """An error event implementation for Terminal."""

    def getThrowable(self):
        """Gets the contained throwable, the cause of the error."""
        pass


class ErrorListener(object):
    """Interface for listening to Terminal errors."""

    def terminalError(self, event):
        """Invoked when a terminal error occurs.

        @param event
                   the fired event.
        """
        pass
