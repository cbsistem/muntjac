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

# from java.io.Serializable import (Serializable,)
# from java.util.Map import (Map,)


class VariableOwner(Serializable):
    """<p>
    Listener interface for UI variable changes. The user communicates with the
    application using the so-called <i>variables</i>. When the user makes a
    change using the UI the terminal trasmits the changed variables to the
    application, and the components owning those variables may then process those
    changes.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def changeVariables(self, source, variables):
        """Called when one or more variables handled by the implementing class are
        changed.

        @param source
                   the Source of the variable change. This is the origin of the
                   event. For example in Web Adapter this is the request.
        @param variables
                   the Mapping from variable names to new variable values.
        """
        pass

    def isEnabled(self):
        """<p>
        Tests if the variable owner is enabled or not. The terminal should not
        send any variable changes to disabled variable owners.
        </p>

        @return <code>true</code> if the variable owner is enabled,
                <code>false</code> if not
        """
        pass

    def isImmediate(self):
        """<p>
        Tests if the variable owner is in immediate mode or not. Being in
        immediate mode means that all variable changes are required to be sent
        back from the terminal immediately when they occur.
        </p>

        <p>
        <strong>Note:</strong> <code>VariableOwner</code> does not include a set-
        method for the immediateness property. This is because not all
        VariableOwners wish to offer the functionality. Such VariableOwners are
        never in the immediate mode, thus they always return <code>false</code>
        in {@link #isImmediate()}.
        </p>

        @return <code>true</code> if the component is in immediate mode,
                <code>false</code> if not.
        """
        pass

    class ErrorEvent(Terminal.ErrorEvent):
        """VariableOwner error event."""

        def getVariableOwner(self):
            """Gets the source VariableOwner.

            @return the variable owner.
            """
            pass
