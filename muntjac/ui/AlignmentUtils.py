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

from muntjac.ui.Alignment import Alignment
from muntjac.ui.ILayout import IAlignmentHandler


class AlignmentUtils(object):
    """Helper class for setting alignments using a short notation.

    Supported notation is:

    t,top for top alignment

    m,middle for vertical center alignment

    b,bottom for bottom alignment

    l,left for left alignment

    c,center for horizontal center alignment

    r,right for right alignment

    @deprecated replaced by {@link Alignment}.
    """

    raise DeprecationWarning, 'AlignmentUtils replaced by Alignment'

    _horizontalMask = (IAlignmentHandler.ALIGNMENT_LEFT
                | IAlignmentHandler.ALIGNMENT_HORIZONTAL_CENTER
                | IAlignmentHandler.ALIGNMENT_RIGHT)

    _verticalMask = (IAlignmentHandler.ALIGNMENT_TOP
                | IAlignmentHandler.ALIGNMENT_VERTICAL_CENTER
                | IAlignmentHandler.ALIGNMENT_BOTTOM)

    _alignmentStrings = dict()

    @classmethod
    def addMapping(cls, alignment, *values):
        for s in values:
            cls._alignmentStrings[s] = alignment


    addMapping(IAlignmentHandler.ALIGNMENT_TOP, 't', 'top')
    addMapping(IAlignmentHandler.ALIGNMENT_BOTTOM, 'b', 'bottom')
    addMapping(IAlignmentHandler.ALIGNMENT_VERTICAL_CENTER, 'm', 'middle')
    addMapping(IAlignmentHandler.ALIGNMENT_LEFT, 'l', 'left')
    addMapping(IAlignmentHandler.ALIGNMENT_RIGHT, 'r', 'right')
    addMapping(IAlignmentHandler.ALIGNMENT_HORIZONTAL_CENTER, 'c', 'center')


    @classmethod
    def setComponentAlignment(cls, parent, component, alignment):
        """Set the alignment for the component using short notation

        @param parent
        @param component
        @param alignment
                   String containing one or two alignment strings. If short
                   notation "r","t",etc is used valid strings include
                   "r","rt","tr","t". If the longer notation is used the
                   alignments should be separated by a space e.g.
                   "right","right top","top right","top". It is valid to mix
                   short and long notation but they must be separated by a
                   space e.g. "r top".
        @throws ValueError
        """
        if alignment is None or len(alignment) == 0:
            raise ValueError, ('alignment for setComponentAlignment() '
                    'cannot be null or empty')

        currentAlignment = parent.getComponentAlignment(
                component).getBitMask()

        if len(alignment) == 1:
            # Use short form "t","l",...
            currentAlignment = cls.parseAlignment(alignment[:1],
                    currentAlignment)

        elif len(alignment) == 2:
            # Use short form "tr","lb",...
            currentAlignment = cls.parseAlignment(alignment[:1],
                    currentAlignment)
            currentAlignment = cls.parseAlignment(alignment[1:2],
                    currentAlignment)

        else:
            # Alignments are separated by space
            strings = alignment.split(' ')
            if len(strings) > 2:
                raise ValueError, ('alignment for setComponentAlignment() '
                        'should not contain more than 2 alignments')

            for alignmentString in strings:
                currentAlignment = cls.parseAlignment(alignmentString,
                        currentAlignment)

        horizontalAlignment = currentAlignment & cls._horizontalMask
        verticalAlignment = currentAlignment & cls._verticalMask
        parent.setComponentAlignment(component,
                Alignment(horizontalAlignment + verticalAlignment))


    @classmethod
    def parseAlignment(cls, alignmentString, alignment):
        """Parse alignmentString which contains one alignment (horizontal
        or vertical) and return and updated version of the passed alignment
        where the alignment in one direction has been changed. If the passed
        alignmentString is unknown an exception is thrown

        @param alignmentString
        @param alignment
        @return
        @throws IllegalArgumentException
        """
        parsed = cls._alignmentStrings.get( alignmentString.lower() )

        if parsed is None:
            raise ValueError, ('Could not parse alignment string \''
                    + alignmentString + '\'')

        if parsed & cls._horizontalMask != 0:
            # Get the vertical alignment from the current alignment
            vertical = alignment & cls._verticalMask
            # Add the parsed horizontal alignment
            alignment = vertical | parsed

        else:
            # Get the horizontal alignment from the current alignment
            horizontal = alignment & cls._horizontalMask
            # Add the parsed vertical alignment
            alignment = horizontal | parsed

        return alignment
