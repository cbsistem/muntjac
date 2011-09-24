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

from muntjac.ui.AbstractOrderedLayout import AbstractOrderedLayout
from muntjac.terminal.gwt.client.ui.VVerticalLayout import VVerticalLayout
from muntjac.ui.ClientWidget import LoadStyle


class VerticalLayout(AbstractOrderedLayout):
    """Vertical layout

    <code>VerticalLayout</code> is a component container, which shows the
    subcomponents in the order of their addition (vertically). A vertical layout
    is by default 100% wide.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.3
    """

    CLIENT_WIDGET = VVerticalLayout
    LOAD_STYLE = LoadStyle.EAGER

    def __init__(self):
        self.setWidth('100%')
