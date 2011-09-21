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

import sys

from muntjac.terminal.ErrorMessage import ErrorMessage


class CompositeErrorMessage(ErrorMessage):
    """Class for combining multiple error messages together.

    @author IT Mill Ltd
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self, errorMessages):
        """Constructor for CompositeErrorMessage.

        @param errorMessages
                   the Collection of error messages that are listed together. At
                   least one message is required.
        """
        # Array of all the errors.
        self._errors = None
        # Level of the error.
        self._level = None

        self._errors = list()
        self._level = -sys.maxint - 1
        for m in errorMessages:
            self.addErrorMessage(m)

        if len(self._errors) == 0:
            raise ValueError, 'Composite error message must have at least one error'


    def getErrorLevel(self):
        """The error level is the largest error level in

        @see com.vaadin.terminal.ErrorMessage#getErrorLevel()
        """
        return self._level


    def addErrorMessage(self, error):
        """Adds a error message into this composite message. Updates the level
        field.

        @param error
                   the error message to be added. Duplicate errors are ignored.
        """
        if error is not None and error not in self._errors:
            self._errors.append(error)
            l = error.getErrorLevel()
            if l > self._level:
                self._level = l


    def iterator(self):
        """Gets Error Iterator.

        @return the error iterator.
        """
        return iter(self._errors)


    def paint(self, target):
        """@see muntjac.terminal.Paintable#paint(muntjac.terminal.PaintTarget)"""
        # Documented in super interface
        if len(self._errors) == 1:
            self._errors[0].paint(target)
        else:
            target.startTag('error')

            if self._level > 0 and self._level <= ErrorMessage.INFORMATION:
                target.addAttribute('level', 'info')
            elif self._level <= ErrorMessage.WARNING:
                target.addAttribute('level', 'warning')
            elif self._level <= ErrorMessage.ERROR:
                target.addAttribute('level', 'error')
            elif self._level <= ErrorMessage.CRITICAL:
                target.addAttribute('level', 'critical')
            else:
                target.addAttribute('level', 'system')
            # Paint all the exceptions
            for error in self._errors:
                error.paint(target)

            target.endTag('error')


    def addListener(self, listener):
        # Documented in super interface
        pass


    def removeListener(self, listener):
        # Documented in super interface
        pass


    def requestRepaint(self):
        # Documented in super interface
        pass


    def requestRepaintRequests(self):
        pass


    def toString(self):
        """Returns a comma separated list of the error messages.

        @return String, comma separated list of error messages.
        """
        retval = '['
        pos = 0
        for error in self._errors:
            if pos > 0:
                retval += ','
            pos += 1
            retval += str(error)
        retval += ']'
        return retval


    def getDebugId(self):
        return None


    def setDebugId(self, idd):
        raise NotImplementedError, 'Setting testing id for this Paintable is not implemented'
