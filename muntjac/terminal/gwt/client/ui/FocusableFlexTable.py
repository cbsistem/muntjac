# -*- coding: utf-8 -*-
from com.vaadin.terminal.gwt.client.Focusable import (Focusable,)
# from com.google.gwt.event.dom.client.BlurEvent import (BlurEvent,)
# from com.google.gwt.event.dom.client.BlurHandler import (BlurHandler,)
# from com.google.gwt.event.dom.client.FocusEvent import (FocusEvent,)
# from com.google.gwt.event.dom.client.FocusHandler import (FocusHandler,)
# from com.google.gwt.event.dom.client.HasBlurHandlers import (HasBlurHandlers,)
# from com.google.gwt.event.dom.client.HasFocusHandlers import (HasFocusHandlers,)
# from com.google.gwt.event.dom.client.HasKeyDownHandlers import (HasKeyDownHandlers,)
# from com.google.gwt.event.dom.client.HasKeyPressHandlers import (HasKeyPressHandlers,)
# from com.google.gwt.event.dom.client.KeyDownEvent import (KeyDownEvent,)
# from com.google.gwt.event.dom.client.KeyDownHandler import (KeyDownHandler,)
# from com.google.gwt.event.dom.client.KeyPressEvent import (KeyPressEvent,)
# from com.google.gwt.event.dom.client.KeyPressHandler import (KeyPressHandler,)
# from com.google.gwt.user.client.ui.FlexTable import (FlexTable,)
# from com.google.gwt.user.client.ui.impl.FocusImpl import (FocusImpl,)


class FocusableFlexTable(FlexTable, HasFocusHandlers, HasBlurHandlers, HasKeyDownHandlers, HasKeyPressHandlers, Focusable):
    """Adds keyboard focus to {@link FlexPanel}."""

    def __init__(self):
        """Default constructor."""
        # make focusable, as we don't need access key magic we don't need to
        # use FocusImpl.createFocusable
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.HasFocusHandlers#addFocusHandler(com.
        # google.gwt.event.dom.client.FocusHandler)

        self.getElement().setTabIndex(0)

    def addFocusHandler(self, handler):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.HasBlurHandlers#addBlurHandler(com.google
        # .gwt.event.dom.client.BlurHandler)

        return self.addDomHandler(handler, FocusEvent.getType())

    def addBlurHandler(self, handler):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.HasKeyDownHandlers#addKeyDownHandler(
        # com.google.gwt.event.dom.client.KeyDownHandler)

        return self.addDomHandler(handler, BlurEvent.getType())

    def addKeyDownHandler(self, handler):
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.HasKeyPressHandlers#addKeyPressHandler
        # (com.google.gwt.event.dom.client.KeyPressHandler)

        return self.addDomHandler(handler, KeyDownEvent.getType())

    def addKeyPressHandler(self, handler):
        return self.addDomHandler(handler, KeyPressEvent.getType())

    def setFocus(self, focus):
        """Sets the keyboard focus to the panel

        @param focus
                   Should the panel have keyboard focus. If true the keyboard
                   focus will be moved to the
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.terminal.gwt.client.Focusable#focus()

        if focus:
            FocusImpl.getFocusImplForPanel().focus(self.getElement())
        else:
            FocusImpl.getFocusImplForPanel().blur(self.getElement())

    def focus(self):
        self.setFocus(True)
