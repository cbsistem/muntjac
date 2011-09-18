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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.ui.DateField import (DateField,)
# from java.util.Date import (Date,)


class PopupDateField(DateField):
    """<p>
    A date entry component, which displays the actual date selector as a popup.

    </p>

    @see DateField
    @see InlineDateField
    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.0
    """
    _inputPrompt = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(PopupDateField, self)()
        elif _1 == 1:
            if isinstance(_0[0], Property):
                dataSource, = _0
                super(PopupDateField, self)(dataSource)
            else:
                caption, = _0
                super(PopupDateField, self)(caption)
        elif _1 == 2:
            if isinstance(_0[1], Date):
                caption, value = _0
                super(PopupDateField, self)(caption, value)
            else:
                caption, dataSource = _0
                super(PopupDateField, self)(caption, dataSource)
        else:
            raise ARGERROR(0, 2)

    def paintContent(self, target):
        super(PopupDateField, self).paintContent(target)
        if self._inputPrompt is not None:
            target.addAttribute('prompt', self._inputPrompt)

    def getInputPrompt(self):
        """Gets the current input prompt.

        @see #setInputPrompt(String)
        @return the current input prompt, or null if not enabled
        """
        return self._inputPrompt

    def setInputPrompt(self, inputPrompt):
        """Sets the input prompt - a textual prompt that is displayed when the field
        would otherwise be empty, to prompt the user for input.

        @param inputPrompt
        """
        self._inputPrompt = inputPrompt
        self.requestRepaint()
